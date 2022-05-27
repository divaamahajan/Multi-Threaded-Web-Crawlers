import threading

class MonitorCrawlers():
    # Initialising a condition class object
    condition_obj = threading.Condition()
    def __init__(self,frontier_size):
        self.size = frontier_size
        self.frontier = [None] * self.size
        self.count = self.lo = self.hi = 0


    def insert(self,url):
        self.condition_obj.acquire()
        while (self.count == self.size) :
        # if (self.count == self.size) :
            self.condition_obj.wait(2)          # if the frontier is full, go to sleep        
        self.frontier[self.hi] = url            # insert an URL into the frontier
        self.hi = (self.hi + 1) % self.size     # slot to place next URL in
        self.count += 1                 
        # one more URL in the frontier now
        # if (self.count == 1) :
        self.condition_obj.notify()
        self.condition_obj.release()

    def remove(self):
        self.condition_obj.acquire()
        while (self.count == 0) :
            self.condition_obj.wait(2)  # if the frontier is empty, go to sleep
        url = self.frontier[self.lo]    # fetch a url from the frontier
        self.frontier[self.lo] = None
        self.lo = (self.lo + 1) % self.size # slot to fetch next url from
        self.count -= 1
        # # one few urls in the frontier
        # if (self.count == (self.size - 1)) :
        self.condition_obj.notify()
        self.condition_obj.release()
        return (url)
        
    def release_locks(self):
        self.condition_obj.release()

