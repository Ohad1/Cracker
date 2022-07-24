from Logger.crack_logger import logger
import Constants
from Master.Job import Job
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
    def __init__(self, hashes, minions, master_url):
        self.hashes = hashes
        self.minions = minions
        self.master_url = master_url
        self.name = 'JOB_EXECUTOR'
        self.num_of_minions = len(self.minions)
        self.num_of_hashes = len(self.hashes)
        self.max_workers = self.num_of_minions * self.num_of_hashes

    def get_ranges(self):
        return [((Constants.NUMBER_RANGE ** Constants.NUMBER_SIZE) * i // self.num_of_minions,
                 (Constants.NUMBER_RANGE ** Constants.NUMBER_SIZE) * (i + 1) // self.num_of_minions)
                for i in range(self.num_of_minions)]

    def add_entry(self, hash_str, number):
        session = FuturesSession()
        session.get(f'http://{self.master_url}/add_entry?hash_str={hash_str}&number={number}', headers=headers)

    async def execute_jobs(self):
        try:
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
                logger.info(f'[{self.name}] {resp_json = }, {url = }, {str(job) = }')
                job.done()
                if 'phone_number' in resp_json:
                    logger.info(f'[{self.name}] Stop execution for hash {job.hash_str}')
                    jobs_to_stop = [cur_job for cur_job in jobs if
                                    cur_job.hash_str == job.hash_str and not cur_job.is_done]
                    if jobs_to_stop:
                        await stop_jobs(jobs_to_stop)
                    hashes_to_numbers[job.hash_str] = resp_json['phone_number']
                    self.add_entry(job.hash_str, resp_json['phone_number'])
            logger.info(f'[{self.name}] {hashes_to_numbers = }')
            return {'message': hashes_to_numbers}, 200
        except ConnectionResetError:
            return {'error': 'Connection with server was reset'}, 500
        except Exception as e:
            return {'error': f'Unknown has occurred: {e}'}, 400
