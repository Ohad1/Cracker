from DB import DB
from LRUCache import LRUCache


class StorageManager:
    def __init__(self, db_conf, cache_size):
        self.db = DB(db_conf)
        self.cache = LRUCache(cache_size)

    def find_number(self, hash_str):
        val = self.cache.get(hash_str)
        return val if val else self.db.find_number(hash_str)

    def update_hashes(self, hashes_to_numbers):
        for hash_str, number in hashes_to_numbers.items():
            self.cache.put(hash_str, number)
        self.db.insert_hashes(list(hashes_to_numbers.items()))
