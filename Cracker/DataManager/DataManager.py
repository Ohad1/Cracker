from DataManager.DB import DB
from DataManager.LRUCache import LRUCache


class DataManager:
    def __init__(self, db_conf, cache_size):
        self.db = DB(db_conf)
        self.cache = LRUCache(cache_size)

    def find_number(self, hash_str):
        val = self.cache.get(hash_str)
        if val:
            return val
        number = self.db.find_number(hash_str)
        if number:
            self.cache.put(hash_str, number)
        return number

    def insert_hashes(self, hashes_to_numbers):
        for hash_str, number in hashes_to_numbers.items():
            self.cache.put(hash_str, number)
        return self.db.insert_hashes(list(hashes_to_numbers.items()))
