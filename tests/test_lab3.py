import unittest
import os
from backend.rc5_algorithm import RC5FileProtector


class TestRC5Algorithm(unittest.TestCase):
    def setUp(self):
        self.password = "SecurePassword123"
        self.protector = RC5FileProtector(self.password)

        self.original_file = "test_secret.txt"
        self.encrypted_file = "test_secret.enc"
        self.decrypted_file = "test_secret_decrypted.txt"

        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write("Це таємний текст для перевірки")

    def tearDown(self):
        for file in [self.original_file, self.encrypted_file, self.decrypted_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_encryption_decryption_cycle(self):
        self.protector.encrypt_file(self.original_file, self.encrypted_file)
        self.assertTrue(os.path.exists(self.encrypted_file))

        self.protector.decrypt_file(self.encrypted_file, self.decrypted_file)
        self.assertTrue(os.path.exists(self.decrypted_file))

        with open(self.decrypted_file, "r", encoding="utf-8") as f:
            result_text = f.read()

        self.assertEqual(result_text, "Це таємний текст для перевірки")

    def test_wrong_password_raises_error(self):
        self.protector.encrypt_file(self.original_file, self.encrypted_file)

        hacker_protector = RC5FileProtector("WrongPassword")

        with self.assertRaises(ValueError):
            hacker_protector.decrypt_file(self.encrypted_file, self.decrypted_file)


if __name__ == '__main__':
    unittest.main()