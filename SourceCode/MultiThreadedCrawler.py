from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import input_parser
from datetime import datetime
import re
from semaphorelock import SemaphporeCrawlers
from monitorlock import MonitorCrawlers

class MultiThreadedCrawler:
    FRONTIER_SIZE = 10
    CRAWLER_DEPTH = 100

    def __init__(self, seed_url, num_threads,locking_option):
        self.seed_url = seed_url
        self.number_of_threads = num_threads
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme, urlparse(self.seed_url).netloc,urlparse(self.seed_url).path)
        # To execute the crawl frontier task concurrently max workers as no of threads at a time
        self.visited_links = set([]) # List to maintain the history of visited links to avoid duplicate visits 
        self.visited_links.add("ROOT")
        # self.frontier_queue = Queue()
        self.frontier_queue = [None] * self.FRONTIER_SIZE   
        self.idx_put = self.idx_pop = int(0)
        self.lock_sem = SemaphporeCrawlers()
        self.lock_mon = MonitorCrawlers(self.FRONTIER_SIZE)
        self.lockfree = False
        self.semaphorelock = False
        self.monitorlock = False   
        if locking_option == 2:
            self.semaphorelock = True
        elif locking_option == 3:
            self.monitorlock = True  
        else:            
            self.lockfree = True      
        self.add_urls_to_frontier(self.seed_url)
        


    def parse_links(self, html):
        ''' For extracting the links
        returns a list of items that contain all the anchor tags present in the webpage.
            Relative URL: URL Without root URL and protocol names.
            Absolute URLs: URL With protocol name, Root URL, Document name.'''
        soup = BeautifulSoup(html, 'html.parser')
        Anchor_Tags = soup.find_all('a', href=True)
        for link in Anchor_Tags:
            # For each anchor tag, retrieve the value associated with href in the tag using Link[‘href’]. 
            url = link['href']
            # If it is a Relative URL change it to an absolute URL 
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                # Filter unvisited URL and put it in frontier queue
                if url not in self.visited_links:
                    self.add_urls_to_frontier(url)

    def add_urls_to_frontier(self, url):
        # it blocks at most timeout seconds and raises the Full exception if no free slot was available within that time. 
        try:
            if self.lockfree:
                # self.frontier_queue.put(url,timeout=60)
                self.frontier_queue[self.idx_put] = url
                self.idx_put = (self.idx_put + 1) % self.FRONTIER_SIZE
            elif self.semaphorelock:
                self.lock_sem.semaphore_frontier()
            elif self.monitorlock:
                self.lock_mon.insert(url)
        except Exception as error:
            print("Writer: Timeout occurred {}".format(str(error)))

    def get_urls_from_frontier(self):       
        # it blocks at most timeout seconds and raises the Empty exception if no item was available within that time.
        try:
            # return self.frontier_queue.get(timeout=60)
            if self.lockfree:
                # self.frontier_queue.put(url,timeout=60)
                url = self.frontier_queue[self.idx_pop]
                self.frontier_queue[self.idx_pop] = None
                self.idx_pop = (self.idx_pop + 1) % self.FRONTIER_SIZE
            elif self.semaphorelock:
                self.lock_sem.semaphore_frontier()
            elif self.monitorlock:
                url = self.lock_mon.remove()
            return url
        except Exception as error:
            print("Writer: Timeout occurred {}".format(str(error)))
              

    def metadata(self, html , url):  # To format the web data into traversible structure
        '''For extracting the content
        Pass the webpage data into BeautifulSoap which helps us to format the messy web data 
        by fixing bad HTML and present to us in an easily-traversible structure.'''
        soup = BeautifulSoup(html, "html.parser")
        web_page_paragraph_contents = soup('p')
        # text = ''
        url = url.replace("https://", "")
        url = re.sub('[^a-zA-Z0-9 \n\.]', '', url)
        output_path = input_parser.get_file_path('MetaData'+ datetime.now().strftime("%d%b%Y_%H00pm"), url + '.txt')       
        with open(output_path, "a") as external_file:
            for para in web_page_paragraph_contents:
                if not ('https:' in str(para.text)):
                    # text = text + str(para.text).strip()                     
                    try:
                        print(str(para.text).strip(), file=external_file)
                    except:
                        continue
            external_file.close()
        return

    def parser_filter(self, thread_job_obj):
        api_response = thread_job_obj.result()
        if api_response and api_response.status_code == 200:
            self.parse_links(api_response.text)
            self.metadata(api_response.text , api_response.url)

    def get_response_from_requests_api(self, url):
        '''Using the handshaking method 
        place the request and set default time as 3 and maximum time as 30
        Once the request is successful return the result set.'''
        try:
            resulturl = requests.get(url, timeout=(3, 30))
            print(f"\n{threading.current_thread().getName()} executing...") 
            return resulturl
        except requests.RequestException:
            return

    def run_web_crawler(self):
      with ThreadPoolExecutor(max_workers=self.number_of_threads,thread_name_prefix='CrawlerThread') as pool_of_crawler_threads:
        while True:
        # while True:
            try:
                target_url = self.get_urls_from_frontier()  
                # get the url from the frontier queue and see if it is already visited or not.
                if target_url not in self.visited_links:
                    # Format the current  URL and add it to history of visited pages 
                    print("Visited URL: {}".format(target_url))
                    if "ROOT" in self.visited_links:
                        self.visited_links.remove("ROOT")
                    self.visited_links.add(target_url)
                    # call function get_response_from_requests_api for target_URL from a pool_of_crawler_threads_of_threads of threads 
                    crawler_thread_job = pool_of_crawler_threads.submit(self.get_response_from_requests_api, target_url)
                    # as corresponding thread job has settled call parser filter
                    crawler_thread_job.add_done_callback(self.parser_filter)
                if len(self.visited_links) >= self.CRAWLER_DEPTH:
                    break
 

            except Empty:
                print("No more links found...")
                return
            except Exception as e:
                print("Reason:")
                print(e)
                continue

  
    def info(self):
        out_dic = dict()
        out_dic['seed'] = self.seed_url
        out_dic['crawled pages'] = self.visited_links
        return out_dic