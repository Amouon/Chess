import unittest
from Common.hash_table import HashTable

class HashTableTest(unittest.TestCase):

    def setUp(self):
        """Setup resources before each test."""
        self.hash_table = HashTable()

    def test_initialization(self):
        """Test hash table initialization."""
        self.assertEqual(self.hash_table.size, 101)
        self.assertEqual(len(self.hash_table.table), 101)

    def test_compute_hash(self):
        """Test hash computation."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        hash_value = self.hash_table.compute_hash(fen)
        self.assertTrue(0 <= hash_value < self.hash_table.size)

    def test_store_and_lookup(self):
        """Test storing and looking up FEN strings."""
        fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        value = 0.5
        move = "e4e5"
        self.hash_table.store(fen, value, move)
        self.assertEqual(self.hash_table.lookup(fen), (value, move))

    def test_collision_handling(self):
        """Test handling of hash collisions."""
        fen1 = "rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3"
        fen2 = "rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 4"
        # Ensure these FEN strings compute to the same hash for testing purposes
        self.assertEqual(self.hash_table.compute_hash(fen1), self.hash_table.compute_hash(fen2))
        self.hash_table.store(fen1, 0.6, "d7d6")
        self.hash_table.store(fen2, 0.4, "d5e4")
        self.assertEqual(self.hash_table.lookup(fen1), (0.6, "d7d6"))
        self.assertEqual(self.hash_table.lookup(fen2), (0.4, "d5e4"))

    def test_resize(self):
        """Test resizing of the hash table."""
        # Fill the table to trigger resize
        for i in range(90):  # 70 is just above 0.7 load factor for the initial size of 101
            self.hash_table.store(f"f{i}", 0.5, f"move{i}")
        self.assertTrue(self.hash_table.size > 101)  # Ensure the table was resized
        # Check that an item stored before resizing is still retrievable
        self.assertEqual(self.hash_table.lookup("f1"), (0.5, "move1"))

if __name__ == '__main__':
    unittest.main()
