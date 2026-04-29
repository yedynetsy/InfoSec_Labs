from backend.md5_algorithm import MD5
from backend.lcg_generator import LinearCongruentialGenerator

class RC5:
    def __init__(self, key: bytes):
        self.w = 32
        self.r = 20
        self.b = len(key)

        self.P = 0xB7E15163
        self.Q = 0x9E3779B9

        self.S = self._expand_key(key)

    def _rol(self, val, shift):
        shift %= self.w
        return ((val << shift) & 0xFFFFFFFF) | (val >> (self.w - shift))

    def _ror(self, val, shift):
        shift %= self.w
        return (val >> shift) | ((val << (self.w - shift)) & 0xFFFFFFFF)

    def _expand_key(self, key):
        u = self.w // 8
        c = max(1, (self.b + u - 1) // u)

        # Розбиваємо ключ на слова
        L = [0] * c
        for i in range(self.b - 1, -1, -1):
            L[i // u] = (L[i // u] << 8) + key[i]

        t = 2 * self.r + 2
        S = [0] * t
        S[0] = self.P
        for i in range(1, t):
            S[i] = (S[i - 1] + self.Q) & 0xFFFFFFFF

        i = j = A = B = 0
        for _ in range(3 * max(c, t)):
            A = S[i] = self._rol((S[i] + A + B) & 0xFFFFFFFF, 3)
            B = L[j] = self._rol((L[j] + A + B) & 0xFFFFFFFF, A + B)
            i = (i + 1) % t
            j = (j + 1) % c

        return S

    def encrypt_block(self, data: bytes):
        # Збираємо два числа з 8 байтів
        A = int.from_bytes(data[:4], 'little')
        B = int.from_bytes(data[4:], 'little')

        A = (A + self.S[0]) & 0xFFFFFFFF
        B = (B + self.S[1]) & 0xFFFFFFFF

        for i in range(1, self.r + 1):
            A = (self._rol(A ^ B, B) + self.S[2 * i]) & 0xFFFFFFFF
            B = (self._rol(B ^ A, A) + self.S[2 * i + 1]) & 0xFFFFFFFF

        return A.to_bytes(4, 'little') + B.to_bytes(4, 'little')

    def decrypt_block(self, data: bytes):
        A = int.from_bytes(data[:4], 'little')
        B = int.from_bytes(data[4:], 'little')

        for i in range(self.r, 0, -1):
            B = self._ror((B - self.S[2 * i + 1]) & 0xFFFFFFFF, A) ^ A
            A = self._ror((A - self.S[2 * i]) & 0xFFFFFFFF, B) ^ B

        B = (B - self.S[1]) & 0xFFFFFFFF
        A = (A - self.S[0]) & 0xFFFFFFFF

        return A.to_bytes(4, 'little') + B.to_bytes(4, 'little')


class RC5FileProtector:
    def __init__(self, password: str):
        md5_hash = MD5.hash_data(password.encode('utf-8'))
        self.key = bytes.fromhex(md5_hash)

        self.rc5 = RC5(self.key)
        self.lcg = LinearCongruentialGenerator()

    def _get_iv(self):
        # Збираємо 8 випадкових байтів
        iv = bytearray()
        for _ in range(8):
            iv.append(self.lcg.next_number() & 0xFF)
        return bytes(iv)

    def _xor_bytes(self, b1, b2):
        return bytes(x ^ y for x, y in zip(b1, b2))

    def encrypt_file(self, in_file: str, out_file: str):
        with open(in_file, 'rb') as f:
            data = f.read()

        # Додаєм заповнювач
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len] * pad_len)

        iv = self._get_iv()
        encrypted_iv = self.rc5.encrypt_block(iv)

        ciphertext = bytearray()
        prev_chunk = iv

        for i in range(0, len(data), 8):
            chunk = data[i:i + 8]
            mixed_chunk = self._xor_bytes(chunk, prev_chunk)
            enc_chunk = self.rc5.encrypt_block(mixed_chunk)

            ciphertext.extend(enc_chunk)
            prev_chunk = enc_chunk

        with open(out_file, 'wb') as f:
            f.write(encrypted_iv)
            f.write(ciphertext)

    def decrypt_file(self, in_file: str, out_file: str):
        with open(in_file, 'rb') as f:
            file_data = f.read()

        encrypted_iv = file_data[:8]
        ciphertext = file_data[8:]

        iv = self.rc5.decrypt_block(encrypted_iv)

        plaintext = bytearray()
        prev_chunk = iv

        # Розшифровуємо основні дані
        for i in range(0, len(ciphertext), 8):
            chunk = ciphertext[i:i + 8]

            dec_chunk = self.rc5.decrypt_block(chunk)
            original_chunk = self._xor_bytes(dec_chunk, prev_chunk)

            plaintext.extend(original_chunk)
            prev_chunk = chunk

        pad_len = plaintext[-1]

        if pad_len < 1 or pad_len > 8:
            raise ValueError("Невірний пароль або файл пошкоджено")

        expected_padding = bytes([pad_len] * pad_len)
        if plaintext[-pad_len:] != expected_padding:
            raise ValueError("Невірний пароль")

        plaintext = plaintext[:-pad_len]

        with open(out_file, 'wb') as f:
            f.write(plaintext)