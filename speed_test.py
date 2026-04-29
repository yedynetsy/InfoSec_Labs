import time
import os
from backend.rsa_algorithm import RSAFileProtector
from backend.rc5_algorithm import RC5FileProtector


def run_speed_test():
    print("Початок тесту швидкості")

    test_file = "test_1mb_speed.dat"
    with open(test_file, "wb") as f:
        f.write(os.urandom(1024 * 1024))

    rsa_encrypted = "test_1mb.rsa"
    rc5_encrypted = "test_1mb.rc5"

    try:
        print("\nТестуємо RC5")
        rc5_prot = RC5FileProtector("SpeedTestPassword123")

        start_time_rc5 = time.time()
        rc5_prot.encrypt_file(test_file, rc5_encrypted)
        rc5_time = time.time() - start_time_rc5

        print(f"RC5 зашифрував за: {rc5_time:.4f} секунд")

        print("\nТестуємо RSA")
        rsa_prot = RSAFileProtector(key_size=2048)

        rsa_prot.generate_and_save_keys("speed_priv.pem", "speed_pub.pem")

        start_time_rsa = time.time()
        rsa_prot.encrypt_file(test_file, rsa_encrypted, "speed_pub.pem")
        rsa_time = time.time() - start_time_rsa

        print(f"RSA зашифрував за: {rsa_time:.4f} секунд")

    finally:
        files_to_clean = [
            test_file, rsa_encrypted, rc5_encrypted,
            "speed_priv.pem", "speed_pub.pem"
        ]
        for file in files_to_clean:
            if os.path.exists(file):
                os.remove(file)
        print("\nТимчасові файли видалено")


if __name__ == "__main__":
    run_speed_test()