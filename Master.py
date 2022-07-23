from flask import request
from FlaskAppWrapper import FlaskAppWrapper
from HashValidator import HashValidator
from JobExecutor import JobExecutor
import log


class Master(FlaskAppWrapper):
    def __init__(self, app, default_num_of_minions, minions_urls, **configs):
        self.default_num_of_minions = default_num_of_minions
        self.name = app.name.upper()
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        self.minions = [{'url': url} for url in minions_urls[:self.default_num_of_minions]]

    async def crack(self):
        hashes_arg = request.args.get('hashes')
        hashes = hashes_arg.split(',')
        log.logger.info(f'[{self.name}] hashes: {hashes}')
        hash_validator = HashValidator(hashes)
        if not hash_validator.validate_hashes():
            return 'Invalid hashes provided', 400
        job_executor = JobExecutor(hashes, self.minions)
        res = await job_executor.execute_jobs()
        return '\n'.join(res), 200
