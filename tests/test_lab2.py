import unittest
import os
from backend.md5_algorithm import MD5

class TestMD5Algorithm(unittest.TestCase):

    def test_rfc1321_vectors(self):
        test_vectors = {
            "": "d41d8cd98f00b204e9800998ecf8427e",
            "a": "0cc175b9c0f1b6a831c399e269772661",
            "abc": "900150983cd24fb0d6963f7d28e17f72",
            "message digest": "f96b697d7cb7938d525a2f31aaf161d0",
            "abcdefghijklmnopqrstuvwxyz": "c3fcd3d76192e4007dfb496cca67e13b",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "d174ab98d277d9f5a5611c2c9f419d9f",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57edf4a22be3c955ac49da2e2107b67a"
        }

        for input_text, expected_hash in test_vectors.items():
            with self.subTest(input_text=input_text):
                # Перетворюємо рядок на байти
                calculated_hash = MD5.hash_data(input_text.encode('utf-8'))
                self.assertEqual(calculated_hash, expected_hash)


    def test_hash_file(self):
        test_file = "test_md5_file.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("message digest")

        try:
            calculated_hash = MD5.hash_file(test_file)
            expected_hash = "f96b697d7cb7938d525a2f31aaf161d0"
            self.assertEqual(calculated_hash, expected_hash)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == '__main__':
    unittest.main()