import base64
import hashlib
import json
import secrets
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CurvePoint:
    x: int
    y: int


class ECCCipher:
    # secp256k1 parameters
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    A = 0
    B = 7
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    G = CurvePoint(
        55066263022277343669578718895168534326250603453777594175500187360389116729240,
        32670510020758816978083085130507043184471273380659243275938904335757337482424,
    )

    def __init__(self):
        key_dir = Path(__file__).resolve().parent / "keys"
        key_dir.mkdir(parents=True, exist_ok=True)
        # Use PEM files like RSA (private_key.pem / public_key.pem)
        self.private_key_path = key_dir / "private_key.pem"
        self.public_key_path = key_dir / "public_key.pem"

        # byte length for coordinates/scalars (secp256k1 -> 32 bytes)
        self._byte_len = (self.P.bit_length() + 7) // 8

    def inverse_mod(self, value: int, modulus: int) -> int:
        return pow(value, -1, modulus)

    def is_on_curve(self, point):
        if point is None:
            return True
        return (point.y * point.y - (point.x * point.x * point.x + self.A * point.x + self.B)) % self.P == 0

    def point_neg(self, point):
        if point is None:
            return None
        return CurvePoint(point.x, (-point.y) % self.P)

    def point_add(self, p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            return None

        if p1 == p2:
            slope = (3 * p1.x * p1.x + self.A) * self.inverse_mod(2 * p1.y % self.P, self.P)
        else:
            slope = (p2.y - p1.y) * self.inverse_mod((p2.x - p1.x) % self.P, self.P)

        slope %= self.P
        x3 = (slope * slope - p1.x - p2.x) % self.P
        y3 = (slope * (p1.x - x3) - p1.y) % self.P
        return CurvePoint(x3, y3)

    def scalar_mult(self, scalar: int, point):
        if scalar % self.N == 0 or point is None:
            return None

        result = None
        addend = point
        k = scalar % self.N

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result

    def generate_keys(self):
        private_key = secrets.randbelow(self.N - 1) + 1
        public_key = self.scalar_mult(private_key, self.G)
        # Private: store raw scalar as fixed-length big-endian bytes, wrapped in PEM
        priv_bytes = private_key.to_bytes(self._byte_len, "big")
        self._write_pem(self.private_key_path, "ECC PRIVATE KEY", priv_bytes)

        # Public: use uncompressed point format 0x04 || X || Y
        x_bytes = public_key.x.to_bytes(self._byte_len, "big")
        y_bytes = public_key.y.to_bytes(self._byte_len, "big")
        pub_raw = b"\x04" + x_bytes + y_bytes
        self._write_pem(self.public_key_path, "ECC PUBLIC KEY", pub_raw)

    def load_keys(self):
        # Support both new PEM format and legacy JSON files (migration)
        # Private key
        if self.private_key_path.exists():
            priv_raw = self._read_pem(self.private_key_path)
            if priv_raw is None:
                # maybe legacy json
                raw = json.loads(self.private_key_path.read_text(encoding="utf-8"))
                private_key = int(raw.get("d"))
            else:
                # expect fixed-length big-endian scalar
                private_key = int.from_bytes(priv_raw, "big")
        else:
            raise FileNotFoundError(f"Private key not found: {self.private_key_path}")

        # Public key
        if self.public_key_path.exists():
            pub_raw = self._read_pem(self.public_key_path)
            if pub_raw is None:
                raw = json.loads(self.public_key_path.read_text(encoding="utf-8"))
                public_key = CurvePoint(int(raw.get("x")), int(raw.get("y")))
            else:
                # expect uncompressed form 0x04 || X || Y
                if len(pub_raw) == 1 + 2 * self._byte_len and pub_raw[0] == 0x04:
                    x = int.from_bytes(pub_raw[1 : 1 + self._byte_len], "big")
                    y = int.from_bytes(pub_raw[1 + self._byte_len : 1 + 2 * self._byte_len], "big")
                    public_key = CurvePoint(x, y)
                else:
                    # fallback to attempt JSON
                    raw = json.loads(self.public_key_path.read_text(encoding="utf-8"))
                    public_key = CurvePoint(int(raw.get("x")), int(raw.get("y")))
        else:
            raise FileNotFoundError(f"Public key not found: {self.public_key_path}")

        return private_key, public_key

    # --- PEM helpers ---
    def _wrap_pem(self, header: str, b64: str) -> str:
        lines = [f"-----BEGIN {header}-----"]
        # wrap at 64 chars
        for i in range(0, len(b64), 64):
            lines.append(b64[i : i + 64])
        lines.append(f"-----END {header}-----")
        return "\n".join(lines) + "\n"

    def _write_pem(self, path: Path, header: str, raw_bytes: bytes):
        b64 = base64.b64encode(raw_bytes).decode("ascii")
        content = self._wrap_pem(header, b64)
        path.write_text(content, encoding="utf-8")

    def _read_pem(self, path: Path) -> bytes | None:
        text = path.read_text(encoding="utf-8").strip()
        if text.startswith("-----BEGIN"):
            # extract base64 between header and footer
            parts = text.splitlines()
            # find first line that starts with '-----BEGIN'
            try:
                # assume header/footer present
                b64_lines = [l for l in parts if not l.startswith("-----")]
                b64 = "".join(b64_lines)
                return base64.b64decode(b64)
            except Exception:
                return None
        else:
            return None

    def derive_keystream(self, shared_secret: int, length: int) -> bytes:
        stream = bytearray()
        counter = 0
        seed = shared_secret.to_bytes(32, "big")

        while len(stream) < length:
            block = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
            stream.extend(block)
            counter += 1

        return bytes(stream[:length])

    def encrypt(self, message: str, public_key) -> str:
        plaintext = message.encode("utf-8")
        ephemeral_private = secrets.randbelow(self.N - 1) + 1
        ephemeral_public = self.scalar_mult(ephemeral_private, self.G)
        shared_point = self.scalar_mult(ephemeral_private, public_key)

        if shared_point is None:
            raise ValueError("Failed to derive shared secret")

        keystream = self.derive_keystream(shared_point.x, len(plaintext))
        ciphertext = bytes(a ^ b for a, b in zip(plaintext, keystream))

        payload = {
            "ephemeral_public_key": {"x": str(ephemeral_public.x), "y": str(ephemeral_public.y)},
            "ciphertext": ciphertext.hex(),
        }
        return base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")

    def decrypt(self, encrypted_message: str, private_key: int) -> str:
        payload = json.loads(base64.b64decode(encrypted_message.encode("ascii")).decode("utf-8"))
        ephemeral_public_key = CurvePoint(
            int(payload["ephemeral_public_key"]["x"]),
            int(payload["ephemeral_public_key"]["y"]),
        )
        ciphertext = bytes.fromhex(payload["ciphertext"])
        shared_point = self.scalar_mult(private_key, ephemeral_public_key)

        if shared_point is None:
            raise ValueError("Failed to derive shared secret")

        keystream = self.derive_keystream(shared_point.x, len(ciphertext))
        plaintext = bytes(a ^ b for a, b in zip(ciphertext, keystream))
        return plaintext.decode("utf-8")

    def hash_message(self, message: str) -> int:
        return int.from_bytes(hashlib.sha256(message.encode("utf-8")).digest(), "big") % self.N

    def sign(self, message: str, private_key: int) -> str:
        z = self.hash_message(message)

        while True:
            nonce = secrets.randbelow(self.N - 1) + 1
            point = self.scalar_mult(nonce, self.G)
            if point is None:
                continue

            r = point.x % self.N
            if r == 0:
                continue

            nonce_inv = self.inverse_mod(nonce, self.N)
            s = (nonce_inv * (z + r * private_key)) % self.N
            if s == 0:
                continue

            return f"{r:064x}{s:064x}"

    def verify(self, message: str, signature: str, public_key) -> bool:
        if len(signature) != 128:
            return False

        try:
            r = int(signature[:64], 16)
            s = int(signature[64:], 16)
        except ValueError:
            return False

        if not (1 <= r < self.N and 1 <= s < self.N):
            return False

        z = self.hash_message(message)
        s_inv = self.inverse_mod(s, self.N)
        u1 = (z * s_inv) % self.N
        u2 = (r * s_inv) % self.N
        point = self.point_add(self.scalar_mult(u1, self.G), self.scalar_mult(u2, public_key))

        if point is None:
            return False

        return point.x % self.N == r
