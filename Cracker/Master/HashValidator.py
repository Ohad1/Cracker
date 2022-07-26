import re
from Logger.crack_logger import logger


class HashValidator:
    VALID_HASH_REGEX_EXP = '^[0-9a-fA-F]{32}$'

    def __init__(self, hashes):
        self.hashes = hashes

    def is_valid_hash(self, hash_str):
        match = re.search(self.VALID_HASH_REGEX_EXP, hash_str)
        if match:
            return True
        logger.error(f'[HASH_VALIDATOR] Found invalid hash: {hash_str}')
        return False

    def validate_hashes(self):
        return all(self.is_valid_hash(hash_str) for hash_str in self.hashes)
