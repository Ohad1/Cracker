from flask import request
from FlaskAppWrapper import FlaskAppWrapper
from HashValidator import HashValidator
from JobExecutor import JobExecutor


class Master(FlaskAppWrapper):
    def __init__(self, app, default_num_of_minions, minions_urls, **configs):
        self.default_num_of_minions = default_num_of_minions
        self.app = app
        super().__init__(self.app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        self.minions = [{'url': url} for url in minions_urls[:self.default_num_of_minions]]

    def crack(self):
        hashes_arg = request.args.get('hashes')
        hashes = hashes_arg.split(',')
        hash_validator = HashValidator(hashes)
        if not hash_validator.validate_hashes():
            return 'Invalid hashes provided', 400
        job_executor = JobExecutor(hashes, self.minions)
        res = job_executor.execute_jobs()
        return '\n'.join(res), 200
