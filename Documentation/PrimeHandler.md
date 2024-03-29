### PrimeHandler
- This class is used to generate prime numbers and perform primality tests. It uses the Miller-Rabin test to determine if a number is prime.
- It uses the Miller-Rabin test to determine if a number is prime, which is a probabilistic test that can be made extremely accurate by increasing the number of iterations.
- While this does not guarantee that the number is prime, it is extremely unlikely that a composite number will pass the test for a large number of iterations.
- It's much faster than the classic primality tests, taking considerably less time to determine if a number is prime (example, a 22-digit prime takes approximately 0.0004 seconds vs roughly an hour for the classic tests).

#### Methods
- `calculate_modular_exponent(base, exponent, modulus)`: Function to calculate (base^exponent) % modulus efficiently.
- `perform_miller_rabin_test(reduced_n_minus_one, number)`: Performs a single Miller-Rabin primality test iteration.
- `is_prime(number, iterations)`: Determines if a number is prime using the Miller-Rabin test.
- `generate_prime(starting_point)`: Finds the next prime number greater than the starting point.

#### Example
```python
prime_handler = PrimeHandler()

# Generate a prime number greater than 100
print(prime_handler.generate_prime(100))
# Output: 101

# Check if a number is prime
print(prime_handler.is_prime(101, 10))
# Output: True

```
