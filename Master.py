from flask import request
from FlaskAppWrapper import FlaskAppWrapper
from HashValidator import HashValidator
from JobExecutor import JobExecutor
import log
from StorageManager import StorageManager
import multiprocessing
from run_minion import run_minion


class Master(FlaskAppWrapper):
    MAX_RETRY_COUNT = 3

    def __init__(self, app, default_num_of_minions, minions_urls, db_conf, cache_size, url, **configs):
        self.default_num_of_minions = default_num_of_minions
        self.name = app.name.upper()
        self.url = url
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        self.add_endpoint('/add_entry', 'add_entry', self.add_entry)
        self.minions = {url: multiprocessing.Process(target=run_minion, args=(f'minion_{i + 1}', url))
                        for i, url in enumerate(minions_urls)}
        # self.active_minions = [url for url in minions_urls[:self.default_num_of_minions]]
        self.storage_manager = StorageManager(db_conf, cache_size)

        for minion_proc in list(self.minions.values())[:self.default_num_of_minions]:
            minion_proc.start()

    async def crack(self):
        retry_count = 0
        hashes_arg = request.args.get('hashes')
        hashes = hashes_arg.split(',')
        log.logger.info(f'[{self.name}] crack request received: {hashes = }')
        hash_validator = HashValidator(hashes)
        if not hash_validator.validate_hashes():
            return 'Invalid hashes provided', 400
        while retry_count < self.MAX_RETRY_COUNT:
            hashes_to_numbers = {hash_str: self.storage_manager.find_number(hash_str) for hash_str in hashes}
            missing_hashes = [hash_str for hash_str, number in hashes_to_numbers.items() if not number]
            if not missing_hashes:
                self.storage_manager.update_hashes(hashes_to_numbers)
                return hashes_to_numbers, 200
            active_minions = [url for url, proc in self.minions.items() if proc.is_alive()]
            job_executor = JobExecutor(missing_hashes, active_minions, self.url)
            resp, ret_code = await job_executor.execute_jobs()
            if 'error' not in resp:
                cracked_hashes = resp['message']
                break
            log.logger.error(f'[{self.name}] Received the following error during execution: {resp["error"]}')
            if ret_code != 500:
                return resp, ret_code
            retry_count += 1
            log.logger.info(f'[{self.name}] Retry master crack. {retry_count = }')
        if retry_count == self.MAX_RETRY_COUNT:
            log.logger.error(f'[{self.name}] MAX_RETRY_COUNT reached {retry_count}, abort exection')
            return resp, ret_code
        for missing_hash, number in cracked_hashes.items():
            hashes_to_numbers[missing_hash] = number
        return hashes_to_numbers, 200

    def add_entry(self):
        hash_str = request.args.get('hash_str')
        number = request.args.get('number')
        log.logger.info(f'[{self.name}] add_entry request received: {hash_str = }, {number = }')
        self.storage_manager.update_hashes({hash_str: number})
        return {'message': 'entered entry successfully'}, 200
