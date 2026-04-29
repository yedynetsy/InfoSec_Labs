from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

class RSAFileProtector:
    def __init__(self, key_size=2048):
        self.key_size = key_size

        self.chunk_size = 190
        self.encrypted_chunk_size = 256

    def generate_and_save_keys(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        print("Генерація ключів RSA")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(private_key_path, 'wb') as f:
            f.write(pem_private)

        with open(public_key_path, 'wb') as f:
            f.write(pem_public)

        print(f"Ключі успішно збережено: {private_key_path}, {public_key_path}")

    def load_public_key(self, public_key_path):
        with open(public_key_path, 'rb') as f:
            pemlines = f.read()
        return serialization.load_pem_public_key(pemlines, backend=default_backend())

    def load_private_key(self, private_key_path):
        with open(private_key_path, 'rb') as f:
            pemlines = f.read()
        return serialization.load_pem_private_key(pemlines, password=None, backend=default_backend())

    def encrypt_file(self, in_file, out_file, public_key_path="public_key.pem"):
        public_key = self.load_public_key(public_key_path)

        with open(in_file, 'rb') as f_in, open(out_file, 'wb') as f_out:
            while True:
                chunk = f_in.read(self.chunk_size)
                if not chunk:
                    break

                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(encrypted_chunk)

    def decrypt_file(self, in_file, out_file, private_key_path="private_key.pem"):
        private_key = self.load_private_key(private_key_path)

        with open(in_file, 'rb') as f_in, open(out_file, 'wb') as f_out:
            while True:
                encrypted_chunk = f_in.read(self.encrypted_chunk_size)
                if not encrypted_chunk:
                    break

                decrypted_chunk = private_key.decrypt(
                    encrypted_chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(decrypted_chunk)