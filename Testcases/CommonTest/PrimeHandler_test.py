import unittest

from Common.prime_handler import PrimeHandler


class PrimeHandlerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.prime_handler = PrimeHandler()
    def test_modular_exponent_calculation(self):
        self.assertEqual(self.prime_handler.calculate_modular_exponent(2, 3, 3), 2)
        self.assertEqual(self.prime_handler.calculate_modular_exponent(2, 3, 5), 3)
        self.assertEqual(self.prime_handler.calculate_modular_exponent(2, 3, 7), 1)

    def test_miller_rabin_test(self):
        self.assertEqual(self.prime_handler.perform_miller_rabin_test(3, 7), True)
        self.assertEqual(self.prime_handler.perform_miller_rabin_test(3, 9), True)
        self.assertEqual(self.prime_handler.perform_miller_rabin_test(7, 13), True)
        self.assertEqual(self.prime_handler.perform_miller_rabin_test(7, 15), False)

    def test_is_prime(self):
        self.assertEqual(self.prime_handler.is_prime(1), False)
        self.assertEqual(self.prime_handler.is_prime(3), True)
        self.assertEqual(self.prime_handler.is_prime(4), False)
        self.assertEqual(self.prime_handler.is_prime(1001), False)
        self.assertEqual(self.prime_handler.is_prime(1009), True)

    def test_generate_prime(self):
        self.assertEqual(self.prime_handler.generate_prime(3), 3)
        self.assertEqual(self.prime_handler.generate_prime(4), 5)
        self.assertEqual(self.prime_handler.generate_prime(1000), 1009)

if __name__ == '__main__':
    unittest.main()
