import threading 
import requests
import time 
from bs4 import BeautifulSoup
from urllib.request import urljoin
from urllib.request import urlparse

def crawler(url,soup,container):
        newUrl = set()
        domain = urlparse(url).netloc
        data =  soup.findAll("a")
        externalURL = []
        internalURL =[]
        for item in data:
            href =  item.get("href")
            if href != "" or href != None or href != '#':
                href =   urljoin(url,href)
                hrefParsed = urlparse(href)
                href =hrefParsed.scheme + "://" + hrefParsed.netloc +hrefParsed.path
                final = urlparse(href)
                is_valid = bool(final.scheme) and bool(final.netloc)
                if is_valid and href not in container:
                    if domain not in href and href not in externalURL:
                        externalURL.append(href)
                    elif domain in href and href not in internalURL:
                        internalURL.append(href)
        return internalURL , externalURL
class FailedRequest(threading.Thread):
    def __init__(self,failed_queue,out_queue,max_retry_times,container):
        threading.Thread.__init__(self)
        self.queue =  failed_queue 
        self.out_queue = out_queue
        self.max_retry_times = max_retry_times 
        self.container = container

    def run(self):
        while True:
            url, timeout,retry_times = self.queue.get()
            if retry_times <= self.max_retry_times:
                time.sleep(retry_times*timeout)
                data = requests.get(url=url)
                if data.status_code != 200:
                    self.queue.put((url,timeout,retry_times+1))
                else:
                    soup = BeautifulSoup(data.content,"lxml")
                    internal , external = crawler(url,soup,self.container)
                    self.out_queue.put((internal,external))
            self.queue.task_done()

class WorkerRequest(threading.Thread):
    def __init__(self,queue,failed_queue,out_queue,container):
        threading.Thread.__init__(self)
        self.queue = queue
        self.failed_queue = failed_queue
        self.out_queue = out_queue
        self.container = container
    
    def run(self):
        while True:
            url = self.queue.get()
            data = requests.get(url)
            if data.status_code != 200:
                self.failed_queue.put((url,1,1))
                pass
            else:
                soup = BeautifulSoup(data.content,"lxml")
                internal , external = crawler(url,soup,self.container)
                self.out_queue.put((internal,external))
            self.queue.task_done()
