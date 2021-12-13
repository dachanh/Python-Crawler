import requests
import queue
import threading
from bs4 import BeautifulSoup
from urllib.request import urljoin
from urllib.request import urlparse
from crawler import FailedRequest, WorkerRequest 

class Worker(object):
    def __init__(self,num_worker):
        self.num_worker = num_worker

    def Execute(self,url,level):
        worker_queue = queue.Queue()
        failed_queue = queue.Queue()
        out_queue = queue.Queue()
        out_queue.put(([url],None))
        internal_url = set()
        external_url = set()
        for _ in range(self.num_worker):
            w = WorkerRequest(worker_queue,failed_queue,out_queue,internal_url)
            w.setDaemon(True)
            w.start()
            f_w = FailedRequest(failed_queue,out_queue,3,internal_url)
            f_w.setDaemon(True)
            f_w.start()

        for d in range(level):
            internal,external= out_queue.get()
            if not external is None:
                for sub in internal:
                    internal_url.add(sub)
                for sub in external:
                    external_url.add(sub)
            for link in internal:
                worker_queue.put(link)
            worker_queue.join()
            failed_queue.join()
        return list(internal_url), list(external_url)
