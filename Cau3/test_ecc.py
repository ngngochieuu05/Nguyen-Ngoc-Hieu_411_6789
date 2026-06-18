import unittest
import sys
import os
import json

# Hack to fix compatibility between Flask and Werkzeug on this system
import werkzeug
if not hasattr(werkzeug, "__version__"):
    import importlib.metadata
    try:
        werkzeug.__version__ = importlib.metadata.version("werkzeug")
    except Exception:
        werkzeug.__version__ = "3.0.0"

# Add cipher folder path to the front of sys.path to avoid name collision with GUI script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "cipher", "ecc"))
from ecc_cipher import ECCCipher

class TestECCCipher(unittest.TestCase):
    def setUp(self):
        self.ecc = ECCCipher()

    def test_key_generation_and_loading(self):
        # Generate new keys
        self.ecc.generate_keys()
        
        # Load keys
        private_key, public_key = self.ecc.load_keys()
        
        # Verify private key is an integer in valid range
        self.assertIsInstance(private_key, int)
        self.assertTrue(1 <= private_key < self.ecc.N)
        
        # Verify public key is a CurvePoint on the curve
        self.assertTrue(self.ecc.is_on_curve(public_key))

    def test_encryption_decryption(self):
        # Generate keys
        self.ecc.generate_keys()
        private_key, public_key = self.ecc.load_keys()
        
        message = "Hello, ECC Security!"
        
        # Encrypt
        encrypted = self.ecc.encrypt(message, public_key)
        self.assertNotEqual(encrypted, message)
        
        # Decrypt
        decrypted = self.ecc.decrypt(encrypted, private_key)
        self.assertEqual(decrypted, message)

    def test_signature_verification(self):
        # Generate keys
        self.ecc.generate_keys()
        private_key, public_key = self.ecc.load_keys()
        
        message = "Verify me using ECDSA!"
        
        # Sign
        signature = self.ecc.sign(message, private_key)
        self.assertEqual(len(signature), 128)  # r (64 hex) + s (64 hex)
        
        # Verify correct signature
        is_valid = self.ecc.verify(message, signature, public_key)
        self.assertTrue(is_valid)
        
        # Verify modified message fails verification
        is_valid_modified = self.ecc.verify(message + " modified", signature, public_key)
        self.assertFalse(is_valid_modified)

    def test_negative_scalar_multiplication(self):
        # Verify scalar multiplication with negative values terminates and is correct
        p1 = self.ecc.scalar_mult(-1, self.ecc.G)
        p2 = self.ecc.scalar_mult(self.ecc.N - 1, self.ecc.G)
        self.assertEqual(p1, p2)


class TestECCAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Add Cau3 directory to sys.path so we can import api
        sys.path.insert(0, os.path.dirname(__file__))
        from api import app
        cls.app = app
        cls.client = app.test_client()

    def test_api_flow(self):
        # 1. Generate keys via API
        response = self.client.get("/api/ecc/generate_keys")
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully", response.get_json()["message"])

        # 2. Encrypt via API
        msg = "Hello API"
        response = self.client.post("/api/ecc/encrypt", json={"message": msg})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("encrypted_message", data)
        ciphertext = data["encrypted_message"]

        # 3. Decrypt via API
        response = self.client.post("/api/ecc/decrypt", json={"ciphertext": ciphertext})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("decrypted_message", data)
        self.assertEqual(data["decrypted_message"], msg)

        # 4. Sign via API
        response = self.client.post("/api/ecc/sign", json={"message": msg})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("signature", data)
        signature = data["signature"]

        # 5. Verify via API
        response = self.client.post("/api/ecc/verify", json={"message": msg, "signature": signature})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("is_verified", data)
        self.assertTrue(data["is_verified"])


if __name__ == "__main__":
    unittest.main()
