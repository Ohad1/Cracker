import sqlite3
from Logger.crack_logger import logger


class DB:
    def __init__(self, db_conf):
        self.scheme = db_conf['scheme']
        self.path = db_conf['path']
        try:
            with sqlite3.connect(self.path) as conn:
                with open(self.scheme) as f:
                    conn.executescript(f.read())
        except sqlite3.Error as error:
            logger.error('[DB] Failed to execute startup script', error)

    def find_number(self, hash_str):
        try:
            with sqlite3.connect(self.path) as conn:
                cur = conn.cursor()
                cur.execute('SELECT number FROM hashes WHERE hash=?', (hash_str,))
                row = cur.fetchone()
                if row:
                    number = row[0]
                    logger.info(f'[DB] Found number: {hash_str} -> {number}')
                    return number
                logger.info(f'[DB] Hash not found: {hash_str}')
                return None
        except sqlite3.Error as error:
            logger.error('[DB] Failed selecting hash', error)

    def insert_hashes(self, hashes):
        logger.info(f'[DB] INSERT {hashes = }')
        try:
            with sqlite3.connect(self.path) as conn:
                cur = conn.cursor()
                query = 'INSERT OR IGNORE INTO hashes (hash, number) VALUES (?, ?)'
                cur.executemany(query, hashes)
                conn.commit()
                logger.info(f'[DB] Successfully inserted {cur.rowcount} {"entries" if cur.rowcount != 1 else "entry"}')
        except sqlite3.Error as error:
            logger.error('[DB] Failed to insert multiple records into sqlite table', error)
