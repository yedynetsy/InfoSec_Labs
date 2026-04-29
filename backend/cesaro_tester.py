import math
import random

class CesaroTester:
    @staticmethod
    # Алгоритм Евкліда для знаходження НСД
    def gcd(a, b):
        while b > 0:
            a, b = b, a % b
        return a

    @classmethod
    # Тестує передану послідовність за теоремою Чезаро
    def test_sequence(cls, sequence):
        if len(sequence) < 2:
            return 0.0, 0.0

        coprime_count = 0
        total_pairs = len(sequence) // 2

        for i in range(0, len(sequence) - 1, 2):
            if cls.gcd(sequence[i], sequence[i + 1]) == 1:
                coprime_count += 1

        probability = coprime_count / total_pairs if total_pairs > 0 else 0

        # Обчислення числа pi (запобігаємо діленню на нуль)
        estimated_pi = math.sqrt(6 / probability) if probability > 0 else 0.0

        return probability, estimated_pi

    @classmethod
    # Тестує системний генератор Python
    def test_system_generator(cls, count, m=131071):
        system_sequence = [random.randint(0, m - 1) for _ in range(count)]
        return cls.test_sequence(system_sequence)