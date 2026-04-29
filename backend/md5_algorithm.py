import math

class MD5:
    INIT_A = 0x67452301
    INIT_B = 0xefcdab89
    INIT_C = 0x98badcfe
    INIT_D = 0x10325476

    SHIFT_AMOUNTS = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ]

    SINE_CONSTANTS = [
        int((1 << 32) * abs(math.sin(i))) & 0xffffffff for i in range(1, 65)
    ]

    @staticmethod
    def _left_rotate(value, shift):
        return ((value << shift) | (value >> (32 - shift))) & 0xffffffff

    @staticmethod
    def _pack_length(length_bits):
        return bytes((length_bits >> (8 * i)) & 0xFF for i in range(8))

    @staticmethod
    def _parse_chunk_to_words(chunk):
        words = []
        for i in range(16):
            offset = i * 4
            word = (chunk[offset] |
                    (chunk[offset + 1] << 8) |
                    (chunk[offset + 2] << 16) |
                    (chunk[offset + 3] << 24))
            words.append(word)
        return words

    @staticmethod
    def _registers_to_hex(a, b, c, d):
        result = ""
        for reg in (a, b, c, d):
            for i in range(4):
                byte_val = (reg >> (8 * i)) & 0xFF
                result += f"{byte_val:02x}"
        return result

    @classmethod
    def hash_data(cls, message: bytes) -> str:
        original_bit_length = (8 * len(message)) & 0xffffffffffffffff

        message = bytearray(message)
        message.append(0x80)

        while len(message) % 64 != 56:
            message.append(0x00)

        message.extend(cls._pack_length(original_bit_length))

        hash_a = cls.INIT_A
        hash_b = cls.INIT_B
        hash_c = cls.INIT_C
        hash_d = cls.INIT_D

        for offset in range(0, len(message), 64):
            block = message[offset:offset + 64]
            words = cls._parse_chunk_to_words(block)

            reg_a = hash_a
            reg_b = hash_b
            reg_c = hash_c
            reg_d = hash_d

            for i in range(64):
                if 0 <= i <= 15:
                    mixed_val = (reg_b & reg_c) | (~reg_b & reg_d)
                    word_index = i
                elif 16 <= i <= 31:
                    mixed_val = (reg_d & reg_b) | (~reg_d & reg_c)
                    word_index = (5 * i + 1) % 16
                elif 32 <= i <= 47:
                    mixed_val = reg_b ^ reg_c ^ reg_d
                    word_index = (3 * i + 5) % 16
                else:
                    mixed_val = reg_c ^ (reg_b | ~reg_d)
                    word_index = (7 * i) % 16

                mixed_val = (mixed_val + reg_a + cls.SINE_CONSTANTS[i] + words[word_index]) & 0xffffffff

                reg_a = reg_d
                reg_d = reg_c
                reg_c = reg_b
                reg_b = (reg_b + cls._left_rotate(mixed_val, cls.SHIFT_AMOUNTS[i])) & 0xffffffff

            hash_a = (hash_a + reg_a) & 0xffffffff
            hash_b = (hash_b + reg_b) & 0xffffffff
            hash_c = (hash_c + reg_c) & 0xffffffff
            hash_d = (hash_d + reg_d) & 0xffffffff

        return cls._registers_to_hex(hash_a, hash_b, hash_c, hash_d)

    @classmethod
    def hash_file(cls, filepath: str) -> str:
        with open(filepath, 'rb') as file:
            file_content = file.read()
        return cls.hash_data(file_content)