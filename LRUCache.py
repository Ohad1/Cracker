from collections import OrderedDict
from crack_logger import logger


class LRUCache:
    # initialising capacity
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    # we return the value of the key
    # that is queried in O(1) and return -1 if we
    # don't find the key in out dict / cache.
    # And also move the key to the end
    # to show that it was recently used.
    def get(self, key):
        if key not in self.cache:
            logger.info(f'[CACHE] Hash not found: {key}')
            return None
        else:
            value = self.cache[key]
            self.cache.move_to_end(key)
            logger.info(f'[CACHE] Found number: {key} -> {value}')
            return value

    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
