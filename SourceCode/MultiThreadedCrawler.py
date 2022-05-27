import atexit
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, thread
from monitorlock import MonitorCrawlers
from semaphorelock import SemaphporeCrawlers
from urllib.parse import urljoin, urlparse
import file_parser
import requests
import threading
import time
import textprint as txt

FRONTIER_SIZE = 30
MAX_RUNNING_TIME_SECONDS = 3
class MultiThreadedCrawler:
    def __init__(self, seed_url, num_threads, locking_option, metadata_store):
        self.seed_url = seed_url
        self.number_of_threads = num_threads
        self.root_url = "{}://{}".format(
            urlparse(self.seed_url).scheme,
            urlparse(self.seed_url).netloc,
            urlparse(self.seed_url).path,
        )
        self.exceptions_list = list()
        # To execute the crawl frontier task concurrently max workers as no of threads at a time
        self.visited_links = set(
            []
        )  # List to maintain the history of visited links to avoid duplicate visits
        self.visited_links.add("ROOT")
        # self.frontier_queue = Queue()
        self.frontier_queue = [None] * FRONTIER_SIZE
        self.idx_put = self.idx_pop = int(0)
        self._mutex_lock = threading.Semaphore(1)
        self.lock_sem = SemaphporeCrawlers(FRONTIER_SIZE)
        self.lock_mon = MonitorCrawlers(FRONTIER_SIZE)
        self.store_metadata = False
        self.lockfree = False
        self.semaphorelock = False
        self.monitorlock = False
        self.start_time = time.time()
        if locking_option == 2:
            self.semaphorelock = True
        elif locking_option == 3:
            self.monitorlock = True
        else:
            self.lockfree = True
        
        if metadata_store == 'Y':
            self.store_metadata = True
        self.add_urls_to_frontier(self.seed_url)

    def parse_links(self, html):
        """For extracting the links
        returns a list of items that contain all the anchor tags present in the webpage.
            Relative URL: URL Without root URL and protocol names.
            Absolute URLs: URL With protocol name, Root URL, Document name."""
        soup = BeautifulSoup(html, "html.parser")
        Anchor_Tags = soup.find_all("a", href=True)
        for link in Anchor_Tags:
            # For each anchor tag, retrieve the value associated with href in the tag using Link[‘href’].
            url = link["href"]
            # If it is a Relative URL change it to an absolute URL
            if url.startswith("/") or url.startswith(self.root_url):
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
                self.idx_put = (self.idx_put + 1) % FRONTIER_SIZE
            elif self.semaphorelock:
                self.lock_sem.insert(url)
            elif self.monitorlock:
                self.lock_mon.insert(url)
        except Exception as error:
            print("Writer: Timeout occurred {}".format(str(error)))

    def get_urls_from_frontier(self):
        try:
            # return self.frontier_queue.get(timeout=60)
            if self.lockfree:
                # self.frontier_queue.put(url,timeout=60)
                url = self.frontier_queue[self.idx_pop]
                self.frontier_queue[self.idx_pop] = None
                self.idx_pop = (self.idx_pop + 1) % FRONTIER_SIZE
            elif self.semaphorelock:
                url = self.lock_sem.remove()
            elif self.monitorlock:
                url = self.lock_mon.remove()
            return url
        except Exception as error:
            print("Writer: Timeout occurred {}".format(str(error)))

    def parser_filter(self, thread_job_obj):
        try:
            api_response = thread_job_obj.result()
            if api_response: # and api_response.status_code == 200:
                self.parse_links(api_response.text)
                # if self.store_metadata:
                #     self.metadata(api_response.text, api_response.url)
        except Exception:
            pass

    def get_response_from_requests_api(self, url):
        """Using the handshaking method
        place the request and set default time as 3 and maximum time as 30
        Once the request is successful return the result set."""
        try:
            response = requests.get(url, timeout=(3, 30))
            print(f"\n{threading.current_thread().getName()} executing...")   
            return response
        except requests.RequestException:
            return

    def run_web_crawler(self):
        thread_list = []
        current_time = time.time()
        with ThreadPoolExecutor(
            max_workers=self.number_of_threads, thread_name_prefix="CrawlerThread"
        ) as pool_of_crawler_threads:
            while True:
                try:
                    if current_time - self.start_time >= MAX_RUNNING_TIME_SECONDS:
                        print(
                            "Time out: {} to {}".format(self.start_time, current_time)
                        )        
                        atexit.unregister(thread._python_exit)
                        pool_of_crawler_threads.shutdown = lambda wait: 20
                        break
                    target_url = self.get_urls_from_frontier()
                    if target_url == None:
                        continue
                    # get the url from the frontier queue and see if it is already visited or not.
                    if target_url not in self.visited_links:
                        # Format the current  URL and add it to history of visited pages
                        print("Visited URL: {}".format(target_url))
                        if "ROOT" in self.visited_links:
                            self.visited_links.remove("ROOT")
                        self.visited_links.add(target_url)
                        # call function get_response_from_requests_api for target_URL from a pool_of_crawler_threads_of_threads of threads
                        crawler_thread_job = pool_of_crawler_threads.submit(
                            self.get_response_from_requests_api, target_url
                        )
                        thread_list.append(crawler_thread_job)
                        # as corresponding thread job has settled call parser filter
                        crawler_thread_job.add_done_callback(self.parser_filter)
                    current_time = time.time()
                    
                except Exception as e:
                    print("Reason:")
                    print(e)
                    self.exceptions_list.append([current_time,e])
                    return
            pool_of_crawler_threads.shutdown = lambda wait: 2
            print("Job Finished.")
            return

    def write_output(self,log_filename):
        # Gets the filename and content of the xls file to record all visited links in this run.
        if self.store_metadata:
            visited_links_filename, visited_links_list = self.get_visited_link_info()        
            # Writes a new xls for content_1
            file_parser.create_output_csv_file(
                filename = visited_links_filename, 
                foldername='Metadata',
                rows= visited_links_list
                )
        # Appends a new row to log file
        file_parser.create_output_csv_file(
            filename = log_filename , 
            rows=[self.get_log_row()]
        )


    def write_exceptions(self,exception_filename):
        file_parser.create_output_csv_file(
            filename= exception_filename,
            rows = self.exceptions_list
        )
    def get_visited_link_info(self):
        file_name = "{}Threads_{}_{}links_on{}at{}.csv".format(
            self.number_of_threads,
            txt.lock_option_str(self),
            len(self.visited_links),
            txt.current_date_str(),
            txt.current_time_str(),
        )
        visited_list = []
        for link in self.visited_links:
            visited_list.append([link])
        return file_name, visited_list

    def get_log_row(self):
        return [
            txt.current_date_str() , 
            txt.current_time_str() ,  
            txt.lock_option_str(self) , 
            self.number_of_threads, 
            len(self.visited_links)
            ]

