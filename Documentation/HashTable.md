## Hash Table
- This contains the documentation for the HashTable class.

### Hash Table (HashTable)
- The HashTable class implements a hash table that stores the values and best moves for a given position.
- The hash table uses the FNV-1a hash function and double hashing to reduce collisions.
- The hash table is resized when the load factor exceeds a certain threshold.

#### Properties
- `size`: The size of the hash table.
- `count`: The number of entries in the hash table.
- `load_factor_threshold`: The load factor threshold at which the hash table is resized.
- `table`: The array that stores the entries in the hash table.
- `prime_handler`: An object of the PrimeHandler class that handles prime number generation.
- `fnv_prime`: The prime number used in the FNV-1a hash function.
- `hash1`: The primary hash value.
- `hash2`: The secondary hash value.
- `position`: The key being inserted/searched.

#### Methods
- `compute_fnv1a_hash(position)`: Computes the FNV-1a hash value for the given position.
- `double_hash(hash1, i, position)`: Applies double hashing to reduce collisions.
- `lookup(fen)`: Looks up the value and best move for the given FEN in the hash table.
- `store(fen, value, move)`: Stores the value and best move for the given FEN in the hash table.
- `resize()`: Resizes the hash table when the load factor exceeds the threshold.
- `_next_prime()`: Finds the next prime greater than 2 times the current size.
- `dump()`: Dumps the hash table.
