class LinearCongruentialGenerator:
    def __init__(self, m=131071, a=64, c=21, x0=256):
        self.m = m
        self.a = a
        self.c = c
        self.x0 = x0
        self.current = x0

    # Генерує наступне псевдовипадкове число
    def next_number(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    # Генерує послідовність заданої довжини
    def generate_sequence(self, count):
        self.current = self.x0
        result = []
        for _ in range(count):
            result.append(self.next_number())

        return result

    # Знаходить період функції генерації
    def find_period(self):
        self.current = self.x0
        seen = {self.x0: 0}

        for i in range(1, self.m + 2):
            val = self.next_number()
            if val in seen:
                return i - seen[val]
            seen[val] = i

        return -1  # Запобіжник
