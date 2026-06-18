from pathlib import Path
import rsa


class RSACipher:
    def __init__(self):
        key_dir = Path(__file__).resolve().parent / "keys"
        key_dir.mkdir(parents=True, exist_ok=True)
        self.private_key_path = key_dir / "private_key.pem"
        self.public_key_path = key_dir / "public_key.pem"

        # Auto-generate keys on startup if they don't exist
        if not self.private_key_path.exists() or not self.public_key_path.exists():
            self.generate_keys()

    def generate_keys(self):
        public_key, private_key = rsa.newkeys(1024)

        # Save private key to PEM file
        self.private_key_path.write_bytes(private_key.save_pkcs1("PEM"))

        # Save public key to PEM file
        self.public_key_path.write_bytes(public_key.save_pkcs1("PEM"))

    def load_keys(self):
        private_key = rsa.PrivateKey.load_pkcs1(self.private_key_path.read_bytes())
        public_key = rsa.PublicKey.load_pkcs1(self.public_key_path.read_bytes())
        return private_key, public_key

    def encrypt(self, message: str, key) -> bytes:
        message_bytes = message.encode("utf-8")
        if isinstance(key, rsa.PrivateKey):
            pub_key = rsa.PublicKey(n=key.n, e=key.e)
        else:
            pub_key = key
        return rsa.encrypt(message_bytes, pub_key)

    def decrypt(self, ciphertext: bytes, key) -> str:
        if isinstance(key, rsa.PublicKey):
            raise ValueError("Decryption requires a private key.")
        decrypted_bytes = rsa.decrypt(ciphertext, key)
        return decrypted_bytes.decode("utf-8")

    def sign(self, message: str, private_key: rsa.PrivateKey) -> bytes:
        message_bytes = message.encode("utf-8")
        return rsa.sign(message_bytes, private_key, "SHA-256")

    def verify(self, message: str, signature: bytes, public_key: rsa.PublicKey) -> bool:
        message_bytes = message.encode("utf-8")
        try:
            rsa.verify(message_bytes, signature, public_key)
            return True
        except rsa.VerificationError:
            return False