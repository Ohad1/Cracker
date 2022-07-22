import re


class HashValidator:
    VALID_HASH_REGEX_EXP = '^[0-9a-fA-F]{32}$'

    def __init__(self, hashes):
        self.hashes = hashes

    def is_valid_hash(self, cur_hash):
        return True if re.search(self.VALID_HASH_REGEX_EXP, cur_hash) else False

    def validate_hashes(self):
        return all(self.is_valid_hash(cur_hash) for cur_hash in self.hashes)
