from Common.prime_handler import PrimeHandler


class HashTable:
    def __init__(self, initial_size=101):
        """ Create the hash table

        :param initial_size: The initial size of the hash table (should be a prime number) """
        self.size = initial_size
        self.count = 0
        self.load_factor_threshold = 0.7
        self.table = [None] * self.size
        self.prime_handler = PrimeHandler()

    def compute_fnv1a_hash(self, position: str) -> int:
        hash = 0xcbf29ce484222325
        fnv_prime = 0x100000001b3

        for byte in position.encode('utf-8'):
            hash ^= byte
            hash *= fnv_prime
            hash &= 0xFFFFFFFFFFFFFFFF

        return hash % self.size

    def double_hash(self, hash1: int, i: int, position: str) -> int:
        """ Double hashing implementation to reduce collisions.
        We use a second hash function to calculate the step size.

        :param hash1: The primary hash value
        :param i: The current probe count (collision count)
        :param position: The key being inserted/searched
        :return: The recalculated hash value after applying double hashing
        """
        hash2 = 1 + (self.compute_fnv1a_hash(position) % (self.size - 1))
        return (hash1 + i * hash2) % self.size

    def lookup(self, fen: str):
        """ Look up the value and best move for the given FEN in the hash table

         :param fen: The given FEN
         :return: The value and best move for the position"""
        position = fen.split(' ', 1)[0]
        h = self.compute_fnv1a_hash(position) % self.size
        i = 0

        while self.table[h] is not None:
            if self.table[h][0] == position:
                return self.table[h][1]  # Return the stored value and move
            i += 1
            h = self.double_hash(h, i, position)
        return None

    def store(self, fen: str, value, move):
        """Store the value and best move for the given FEN in the hash table."""
        position = fen.split(' ', 1)[0]
        h = self.compute_fnv1a_hash(position)
        i = 0

        while self.table[h] is not None:
            if self.table[h][0] == position:
                # Replace the existing tuple with a new one that includes the updated value and move
                self.table[h] = (position, (value, move))
                return
            i += 1
            h = self.double_hash(h, i, position)

        # If the position was not found, insert a new entry
        self.table[h] = (position, (value, move))
        self.count += 1
        if self.count / self.size > self.load_factor_threshold:
            self.resize()

    def resize(self):
        """ Resize the hash table once the load factor exceeds the threshold """
        self.size = self._next_prime()
        old_table = self.table
        self.table = [None] * self.size
        self.count = 0

        for entry in old_table:
            if entry is not None:
                position, data = entry
                self.store(position, *data)

    def _next_prime(self) -> int:
        """ Finds the next prime greater than 2 times the current size

        :return: The desired prime
        """

        return self.prime_handler.generate_prime(2 * self.size)

    def dump(self):
        """ Dump the hash table """
        return self.table
