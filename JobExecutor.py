import logging
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from uuid import uuid4
import log


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

    def format_crack_url(self, hash_str, minion, hash_range, hash_uuid):
        start, end = hash_range
        minion_url = minion["url"].replace('0.0.0.0', '127.0.0.1')
        url = f'http://{minion_url}/crack?hash_str={hash_str}&range_start={start}&range_end={end}&hash_uuid={hash_uuid}'
        return url

    def format_stop_url(self, minion, hash_uuid):
        minion_url = minion["url"].replace('0.0.0.0', '127.0.0.1')
        url = f'http://{minion_url}/stop?hash_uuid={hash_uuid}'
        return url

    def execute_job(self, hash_str, minions, ranges):
        # tasks = [asyncio.create_task(self.call_minion(hash_str, minion, hash_range))
        #          for minion, hash_range in zip(minions, ranges)]
        # for res in asyncio.as_completed(tasks):
        #     compl = await res
        # print(f'res: {compl} completed at {time.strftime("%X")}')
        session = FuturesSession()

        urls_to_uuids = {f'{minion["url"]}': str(uuid4()) for minion in minions}
        requests_urls = [self.format_crack_url(hash_str, minion, hash_range, urls_to_uuids[f'{minion["url"]}']) for
                         minion, hash_range in zip(minions, ranges)]
        log.logger.warning(str(requests_urls))
        crack_futures = [session.get(url) for url in requests_urls]
        done_requests = []
        for future in as_completed(crack_futures):
            resp_json = future.result().json()
            url = future.result().request.url
            done_requests.append(url[:url.index('/crack')].replace('http://', ''))
            if 'phone_number' in resp_json:
                log.logger.info('Stop execution')

                requests_urls = [self.format_stop_url(minion, urls_to_uuids[f'{minion["url"]}'])
                                 for minion in minions if minion['url'] not in done_requests]
                log.logger.info(f'{done_requests = }, {requests_urls = }')
                [session.get(url) for url in requests_urls]
                session.executor.shutdown(wait=False, cancel_futures=False)
                return resp_json['phone_number']
        return {'error': 'Hash computation failed. Invalid range given'}

    def execute_jobs(self):
        res = []
        for hash_str in self.hashes:
            ranges = self.get_ranges(len(self.minions))
            res.append(self.execute_job(hash_str, self.minions, ranges))
        return res
