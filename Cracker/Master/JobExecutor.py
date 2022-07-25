import requests
from Logger.crack_logger import logger
from Master.Job import Job
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

headers = {'Content-Type': 'application/json',
           'accept': 'application/json',
           'Connection': 'keep-alive'}


def stop_jobs(jobs_to_stop):
    if not jobs_to_stop:
        return
    session = FuturesSession(max_workers=len(jobs_to_stop))
    for job in jobs_to_stop:
        session.get(job.get_termination_url(), headers=headers)


class JobExecutor:
    DIGIT_RANGE = 10
    NUMBER_LEN = 8
    MAX_WORKERS_COEFFICIENT = 15

    def __init__(self, hashes, minions, master_url):
        self.hashes = hashes
        self.minions = minions
        self.master_url = master_url
        self.name = 'JOB_EXECUTOR'
        self.num_of_minions = len(self.minions)
        self.num_of_hashes = len(self.hashes)
        self.max_workers = self.num_of_minions * max(self.num_of_hashes, self.MAX_WORKERS_COEFFICIENT)
        self.failed_connections_uuids = set()

    def get_ranges(self):
        return [((self.DIGIT_RANGE ** self.NUMBER_LEN) * i // self.num_of_minions,
                 (self.DIGIT_RANGE ** self.NUMBER_LEN) * (i + 1) // self.num_of_minions)
                for i in range(self.num_of_minions)]

    def add_entry(self, hash_str, number):
        session = FuturesSession()
        session.post(f'http://{self.master_url}/decoded_hashes?hash_str={hash_str}',
                     headers=headers,
                     json={hash_str: number})

    def execution_loop(self, futures, urls_to_jobs):
        hashes_to_numbers = {}
        for future in as_completed(futures):
            try:
                resp_json = future.result().json()
                url = future.result().request.url
                job = urls_to_jobs[url]
                logger.info(f'[{self.name}] {resp_json = }, {url = }, {str(job) = }')
                job.stop()
                if 'phone_number' in resp_json:
                    logger.info(f'[{self.name}] Stop execution for hash {job.hash_str}')
                    jobs_to_stop = [cur_job for cur_job in urls_to_jobs.values() if
                                    cur_job.hash_str == job.hash_str and not cur_job.is_done]
                    stop_jobs(jobs_to_stop)
                    hashes_to_numbers[job.hash_str] = resp_json['phone_number']
                    self.add_entry(job.hash_str, resp_json['phone_number'])
            except ConnectionResetError:
                return {'error': 'Connection with server was reset'}
            except requests.exceptions.ConnectionError as e:
                logger.warn(f'[{self.name}] Continue run after ConnectionError: {e.request.url}')
                uuid_index = e.request.url.index('hash_uuid=') + len('hash_uuid=')
                hash_uuid = e.request.url[uuid_index:]
                self.failed_connections_uuids.add(hash_uuid)
                pass
            except Exception as e:
                return {'error': f'Unknown error has occurred: {e}'}
        return hashes_to_numbers

    async def execute_jobs(self):
        ranges = self.get_ranges()
        session = FuturesSession(max_workers=self.max_workers)
        jobs = [Job(hash_str, minion, hash_range)
                for hash_str in self.hashes
                for minion, hash_range in zip(self.minions, ranges)]
        urls_to_jobs = {job.get_execution_url(): job for job in jobs}
        futures = [session.get(url, headers=headers) for url in urls_to_jobs.keys()]
        hashes_to_numbers = self.execution_loop(futures, urls_to_jobs)
        logger.info(f'[{self.name}] {hashes_to_numbers = }')
        if len(hashes_to_numbers) != len(self.hashes):
            jobs_to_stop = [cur_job for cur_job in jobs if
                            cur_job.uuid not in self.failed_connections_uuids and not cur_job.is_done]
            stop_jobs(jobs_to_stop)
            return {'error': f'Could not crack all hashes due to overload: '
                             f'{len(self.hashes)} - {len(hashes_to_numbers)}'
                             f' = {len(self.hashes) - len(hashes_to_numbers)} hashes are missing'}
        return {'message': hashes_to_numbers}
