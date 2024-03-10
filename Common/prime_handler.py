from random import randint


class PrimeHandler:
    @staticmethod
    def calculate_modular_exponent(base: int, exponent: int, modulus: int) -> int:
        """ Function to calculate (base^exponent) % modulus efficiently.
        :param base: The base
        :param exponent: The exponent
        :param modulus: The modulus

        :return: (base^exponent) % modulus """
        result = 1  # Initialize result
        base = base % modulus  # Update x if it is more than or equal to p
        while exponent > 0:
            if exponent & 1:
                result = (result * base) % modulus
            exponent = exponent >> 1  # Equivalent to exponent = exponent / 2
            base = (base * base) % modulus
        return result

    def perform_miller_rabin_test(self, reduced_n_minus_one: int, number: int) -> bool:
        """ Performs a single Miller-Rabin primality test iteration.
        :param reduced_n_minus_one: The reduced n-1
        :param number: The number to test

        :return: True if the number is prime, False otherwise.
        """
        witness = 2 + randint(1, number - 4)  # A random number in [2, number-2]
        x = self.calculate_modular_exponent(witness, reduced_n_minus_one, number)
        if x == 1 or x == number - 1:
            return True
        while reduced_n_minus_one != number - 1:
            x = (x * x) % number
            reduced_n_minus_one *= 2
            if x == 1:
                return False
            if x == number - 1:
                return True
        return False

    def is_prime(self, number: int, iterations: int = 10) -> bool:
        """Determines if a number is prime using the Miller-Rabin test.
        :param number: The number to test
        :param iterations: The number of iterations to perform

        :return: True if the number is prime, False otherwise."""
        if number <= 1 or number == 4:
            return False
        if number <= 3:
            return True
        if number % 2 == 0:
            return False

        reduced_n_minus_one = number - 1
        while reduced_n_minus_one % 2 == 0:
            reduced_n_minus_one //= 2

        for _ in range(iterations):
            if not self.perform_miller_rabin_test(reduced_n_minus_one, number):
                return False
        return True

    def generate_prime(self, starting_point: int):
        """ Finds the next prime number greater than the starting point.
        :param starting_point: The starting point

        :return: The next prime number greater than the starting point """

        if starting_point % 2 == 0:
            starting_point += 1

        while True:
            if self.is_prime(starting_point):
                return starting_point
            starting_point += 2