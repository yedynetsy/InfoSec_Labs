import unittest
from backend.lcg_generator import LinearCongruentialGenerator
from backend.cesaro_tester import CesaroTester

class TestLinearCongruentialGenerator(unittest.TestCase):
    def setUp(self):
        self.lcg = LinearCongruentialGenerator(m=131071, a=64, c=21, x0=256)

    def test_next_number(self):
        # Перевіряємо, чи правильно обчислюється перше число за формулою
        # Розрахунок вручну: (64 * 256 + 21) % 131071 = 16405
        first_number = self.lcg.next_number()
        self.assertEqual(first_number, 16405)

    def test_generate_sequence(self):
        # Перевіряємо генерацію списку заданої довжини
        count = 10
        sequence = self.lcg.generate_sequence(count)
        self.assertEqual(len(sequence), count)
        # Перше число у списку має бути 16405
        self.assertEqual(sequence[0], 16405)

    def test_find_period_small_params(self):
        # Перевіряємо пошук періоду на генераторі з маленькими параметрами
        # Для m=8, a=5, c=1, x0=0 період дорівнює 8
        small_lcg = LinearCongruentialGenerator(m=8, a=5, c=1, x0=0)
        self.assertEqual(small_lcg.find_period(), 8)


class TestCesaroTester(unittest.TestCase):
    def test_gcd(self):
        # Перевіряємо алгоритм Евкліда для знаходження НСД
        self.assertEqual(CesaroTester.gcd(14, 21), 7)
        self.assertEqual(CesaroTester.gcd(13, 27), 1)

    def test_test_sequence(self):
        # Перевіряємо логіку підрахунку ймовірності Чезаро
        # Масив з 4 чисел:
        # 1 пара: (14, 21) - НСД = 7
        # 2 пара: (13, 27) - НСД = 1
        # Отже, ймовірність = 1 з 2 пар = 0.5
        sequence = [14, 21, 13, 27]
        prob, pi_est = CesaroTester.test_sequence(sequence)

        self.assertEqual(prob, 0.5)
        self.assertTrue(pi_est > 0)  # pi має бути розраховано

    def test_system_generator(self):
        # Перевіряємо, чи системний генератор повертає адекватні типи даних
        prob, pi_est = CesaroTester.test_system_generator(100)
        self.assertTrue(0.0 <= prob <= 1.0)
        self.assertIsInstance(pi_est, float)


if __name__ == '__main__':
    unittest.main()