import asyncio
import log
import Constants
from Job import Job
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

headers = {'Content-Type': 'application/json',
           'accept': 'application/json',
           'Connection': 'keep-alive'}


async def stop_jobs(jobs_to_stop):
    session = FuturesSession(max_workers=len(jobs_to_stop))
    for job in jobs_to_stop:
        session.get(job.get_termination_url(), headers=headers)


class JobExecutor:
    def __init__(self, hashes, minions):
        self.hashes = hashes
        self.minions = minions
        self.name = 'JOB_EXECUTOR'
        self.num_of_minions = len(self.minions)
        self.num_of_hashes = len(self.hashes)
        self.max_workers = self.num_of_minions * self.num_of_hashes

    def get_ranges(self):
        return [((Constants.NUMBER_RANGE ** Constants.NUMBER_SIZE) * i // self.num_of_minions,
                 (Constants.NUMBER_RANGE ** Constants.NUMBER_SIZE) * (i + 1) // self.num_of_minions)
                for i in range(self.num_of_minions)]

    async def execute_jobs(self):
        hashes_to_numbers = {}
        ranges = self.get_ranges()
        session = FuturesSession(max_workers=self.max_workers)
        jobs = [Job(hash_str, minion, hash_range)
                for hash_str in self.hashes
                for minion, hash_range in zip(self.minions, ranges)]
        urls_to_jobs = {job.get_execution_url(): job for job in jobs}
        futures = [session.get(url, headers=headers) for url in urls_to_jobs.keys()]
        for future in as_completed(futures):
            resp_json = future.result().json()
            url = future.result().request.url
            job = urls_to_jobs[url]
            log.logger.info(f'[{self.name}] {resp_json = }, {url = }, {str(job) = }')
            job.done()
            if 'phone_number' in resp_json:
                log.logger.info(f'[{self.name}] Stop execution for hash {job.hash_str}')
                jobs_to_stop = [cur_job for cur_job in jobs if cur_job.hash_str == job.hash_str and not cur_job.is_done]
                if jobs_to_stop:
                    await stop_jobs(jobs_to_stop)
                hashes_to_numbers[job.hash_str] = resp_json['phone_number']
        log.logger.info(f'[{self.name}] {hashes_to_numbers = }')
        return hashes_to_numbers
