import os
from cryptography.hazmat.primitives.asymmetric import dsa, utils
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class DSSProtector:
    def __init__(self, key_size=2048):
        self.key_size = key_size

    def generate_and_save_keys(self, private_key_path="dsa_private_key.pem", public_key_path="dsa_public_key.pem"):
        # Генерує пару ключів DSA та зберігає їх у файли PEM
        private_key = dsa.generate_private_key(
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

    def load_private_key(self, private_key_path):
        with open(private_key_path, 'rb') as f:
            pemlines = f.read()
        return serialization.load_pem_private_key(pemlines, password=None, backend=default_backend())

    def load_public_key(self, public_key_path):
        with open(public_key_path, 'rb') as f:
            pemlines = f.read()
        return serialization.load_pem_public_key(pemlines, backend=default_backend())

    def sign_text(self, text: str, private_key_path="dsa_private_key.pem") -> str:
        # Підписує текст і повертає HEX-рядок підпису
        private_key = self.load_private_key(private_key_path)
        data = text.encode('utf-8')

        signature = private_key.sign(
            data,
            hashes.SHA256()
        )
        return signature.hex()

    def verify_text(self, text: str, signature_hex: str, public_key_path="dsa_public_key.pem") -> bool:
        # Перевіряє підпис для тексту
        public_key = self.load_public_key(public_key_path)
        data = text.encode('utf-8')
        signature_bytes = bytes.fromhex(signature_hex)

        try:
            public_key.verify(signature_bytes, data, hashes.SHA256())
            return True
        except Exception:
            return False

    def sign_file(self, filepath: str, sig_filepath: str, private_key_path="dsa_private_key.pem"):
        # Підписує великий файл частинами і зберігає HEX-підпис у файл
        private_key = self.load_private_key(private_key_path)
        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, backend=default_backend())

        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)

        digest = hasher.finalize()

        signature = private_key.sign(
            digest,
            utils.Prehashed(chosen_hash)
        )

        with open(sig_filepath, 'w', encoding='utf-8') as f:
            f.write(signature.hex())

    def verify_file(self, filepath: str, sig_filepath: str, public_key_path="dsa_public_key.pem") -> bool:
        public_key = self.load_public_key(public_key_path)

        with open(sig_filepath, 'r', encoding='utf-8') as f:
            signature_hex = f.read().strip()
        signature_bytes = bytes.fromhex(signature_hex)

        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, backend=default_backend())

        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)

        digest = hasher.finalize()

        try:
            public_key.verify(
                signature_bytes,
                digest,
                utils.Prehashed(chosen_hash)
            )
            return True
        except Exception:
            return False