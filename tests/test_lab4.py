import unittest
import os
from backend.rsa_algorithm import RSAFileProtector

class TestRSAAlgorithm(unittest.TestCase):
    def setUp(self):
        self.protector = RSAFileProtector(key_size=2048)

        self.original_file = "test_rsa_secret.txt"
        self.encrypted_file = "test_rsa_secret.enc"
        self.decrypted_file = "test_rsa_secret_decrypted.txt"
        self.priv_key = "test_private_key.pem"
        self.pub_key = "test_public_key.pem"

        self.test_text = "Це таємний текст для перевірки алгоритму RSA. " * 20
        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write(self.test_text)

    def tearDown(self):
        files_to_remove = [
            self.original_file, self.encrypted_file, self.decrypted_file,
            self.priv_key, self.pub_key
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

    def test_rsa_encryption_decryption_cycle(self):
        self.protector.generate_and_save_keys(self.priv_key, self.pub_key)
        self.assertTrue(os.path.exists(self.priv_key))
        self.assertTrue(os.path.exists(self.pub_key))

        self.protector.encrypt_file(self.original_file, self.encrypted_file, self.pub_key)
        self.assertTrue(os.path.exists(self.encrypted_file))

        self.protector.decrypt_file(self.encrypted_file, self.decrypted_file, self.priv_key)
        self.assertTrue(os.path.exists(self.decrypted_file))

        with open(self.decrypted_file, "r", encoding="utf-8") as f:
            result_text = f.read()

        self.assertEqual(result_text, self.test_text)


if __name__ == '__main__':
    unittest.main()