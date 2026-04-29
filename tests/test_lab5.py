import unittest
import os
from backend.dss_algorithm import DSSProtector


class TestDSSAlgorithm(unittest.TestCase):
    def setUp(self):
        self.protector = DSSProtector(key_size=1024)

        self.test_file = "test_dss_file.txt"
        self.sig_file = "test_dss_file.txt.sig"
        self.priv_key = "test_dsa_private_key.pem"
        self.pub_key = "test_dsa_public_key.pem"

        self.test_text = "Секретне повідомлення для цифрового підпису"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Дані великого файлу для тестування DSS")

    def tearDown(self):
        files_to_remove = [self.test_file, self.sig_file, self.priv_key, self.pub_key]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

    def test_text_signing_verification(self):
        self.protector.generate_and_save_keys(self.priv_key, self.pub_key)
        signature = self.protector.sign_text(self.test_text, self.priv_key)
        is_valid = self.protector.verify_text(self.test_text, signature, self.pub_key)

        self.assertTrue(is_valid)

    def test_file_signing_verification(self):
        # Тест підпису файлу (з хешуванням)
        self.protector.generate_and_save_keys(self.priv_key, self.pub_key)
        self.protector.sign_file(self.test_file, self.sig_file, self.priv_key)

        self.assertTrue(os.path.exists(self.sig_file))

        is_valid = self.protector.verify_file(self.test_file, self.sig_file, self.pub_key)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()