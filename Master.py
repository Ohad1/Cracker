from flask import request
from FlaskAppWrapper import FlaskAppWrapper
from HashValidator import HashValidator
from JobExecutor import JobExecutor
import log
from StorageManager import StorageManager


class Master(FlaskAppWrapper):
    def __init__(self, app, default_num_of_minions, minions_urls, db_conf, cache_size, url, **configs):
        self.default_num_of_minions = default_num_of_minions
        self.name = app.name.upper()
        self.url = url
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        self.add_endpoint('/add_entry', 'add_entry', self.add_entry)
        self.minions = [{'url': url} for url in minions_urls[:self.default_num_of_minions]]
        self.storage_manager = StorageManager(db_conf, cache_size)

    async def crack(self):
        hashes_arg = request.args.get('hashes')
        hashes = hashes_arg.split(',')
        log.logger.info(f'[{self.name}] crack request received: {hashes = }')
        hash_validator = HashValidator(hashes)
        if not hash_validator.validate_hashes():
            return 'Invalid hashes provided', 400
        hashes_to_numbers = {hash_str: self.storage_manager.find_number(hash_str) for hash_str in hashes}
        missing_hashes = [hash_str for hash_str, number in hashes_to_numbers.items() if not number]
        if not missing_hashes:
            self.storage_manager.update_hashes(hashes_to_numbers)
            return hashes_to_numbers, 200
        job_executor = JobExecutor(missing_hashes, self.minions, self.url)
        missing_hashes = await job_executor.execute_jobs()
        for missing_hash, number in missing_hashes.items():
            hashes_to_numbers[missing_hash] = number
        return hashes_to_numbers, 200

    def add_entry(self):
        hash_str = request.args.get('hash_str')
        number = request.args.get('number')
        log.logger.info(f'[{self.name}] add_entry request received: {hash_str = }, {number = }')
        self.storage_manager.update_hashes({hash_str: number})
        return {'message': 'entered entry successfully'}, 200
