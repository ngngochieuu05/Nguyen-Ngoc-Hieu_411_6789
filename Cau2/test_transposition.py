import unittest
from transposition_cipher import encrypt, decrypt

class TestTranspositionCipher(unittest.TestCase):
    def test_digit_key_simple(self):
        # Test Case 1: Digit key "312", message "HELLOWORLD"
        plaintext = "HELLOWORLD"
        key = "312"
        expected_cipher = "EOR LWL HLOD"
        
        cipher = encrypt(plaintext, key)
        self.assertEqual(cipher, expected_cipher)
        
        decrypted = decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_keyword_key(self):
        # Test Case 2: Keyword key "SAFE", message "INFORMATION SECURITY"
        plaintext = "INFORMATION SECURITY"
        key = "SAFE"
        expected_cipher = "NMOEIOT UYFANCTIRISR"
        
        cipher = encrypt(plaintext, key)
        self.assertEqual(cipher, expected_cipher)
        
        decrypted = decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_digit_key_reverse(self):
        # Test Case 3: Digit key "4321", message "SECURITY"
        plaintext = "SECURITY"
        key = "4321"
        expected_cipher = "UYCTEISR"
        
        cipher = encrypt(plaintext, key)
        self.assertEqual(cipher, expected_cipher)
        
        decrypted = decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

    def test_spaces_and_special_chars(self):
        # Test Case 4: Message with punctuation, key "SECRET"
        plaintext = "HELLO, WORLD!"
        key = "SECRET"
        # Key 'SECRET' sorting:
        # S(index 0) -> rank 4
        # E(index 1) -> rank 1
        # C(index 2) -> rank 0
        # R(index 3) -> rank 3
        # E(index 4) -> rank 2
        # T(index 5) -> rank 5
        # Expected sorting order ranks: [4, 1, 0, 3, 2, 5]
        # Padded text length: 18 (HELLO, WORLD!     )
        # Grid:
        # H E L L O ,
        #   W O R L D
        # !          
        # (padded with spaces to length 18)
        # Let's run encryption and check decryption
        cipher = encrypt(plaintext, key)
        decrypted = decrypt(cipher, key)
        self.assertEqual(decrypted, plaintext)

if __name__ == "__main__":
    unittest.main()
