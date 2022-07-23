import logging
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

logging.basicConfig(filename='record.log', level=logging.DEBUG)


class JobExecutor:
    NUMBER_SIZE = 8
    NUMBER_RANGE = 10

    def __init__(self, hashes, minions):
        self.hashes = hashes
        self.minions = minions

    def get_ranges(self, num_of_minions):
        return [((self.NUMBER_RANGE ** self.NUMBER_SIZE) * i // num_of_minions,
                 (self.NUMBER_RANGE ** self.NUMBER_SIZE) * (i + 1) // num_of_minions)
                for i in range(num_of_minions)]

    def get_url(self, hash_str, minion, hash_range):
        start, end = hash_range
        minion_url = minion["url"].replace('0.0.0.0', '127.0.0.1')
        url = f'http://{minion_url}/crack?hash_str={hash_str}&range_start={start}&range_end={end}'
        return url

    def execute_job(self, hash_str, minions, ranges):
        # tasks = [asyncio.create_task(self.call_minion(hash_str, minion, hash_range))
        #          for minion, hash_range in zip(minions, ranges)]
        # for res in asyncio.as_completed(tasks):
        #     compl = await res
        # print(f'res: {compl} completed at {time.strftime("%X")}')
        session = FuturesSession()
        logging.debug(str([self.get_url(hash_str, minion, hash_range) for minion, hash_range in zip(minions, ranges)]))
        futures = [session.get(self.get_url(hash_str, minion, hash_range)) for minion, hash_range in
                   zip(minions, ranges)]
        for future in as_completed(futures):
            resp = future.result().json()
            if 'phone_number' in resp:
                session.executor.shutdown(wait=False)
                return resp['phone_number']
        return {'error': 'Hash computation failed. Invalid range given'}

    def execute_jobs(self):
        res = []
        for hash_str in self.hashes:
            ranges = self.get_ranges(len(self.minions))
            res.append(self.execute_job(hash_str, self.minions, ranges))
        return res
