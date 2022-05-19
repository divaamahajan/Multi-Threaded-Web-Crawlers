<<<<<<< HEAD
import threading

class SemaphporeCrawlers:
    __full_slots = None
    __empty_slots = None
    __mutex_lock = None
    __frontier_queue = None
    __write_idx = __read_idx = 0
    __size = 0

    def __init__(self, queue_size):
        self.__frontier_queue = [None] * queue_size
        self.__empty_slots = threading.Semaphore(queue_size)
        self.__full_slots = threading.Semaphore(0)
        self.__mutex_lock = threading.Semaphore(1)
        self.__size = queue_size


    def insert(self, url):
        self.__empty_slots.acquire()
        self.__mutex_lock.acquire()
        self.__frontier_queue[self.__write_idx] = url
        self.__write_idx = (self.__write_idx + 1) % self.__size
        self.__mutex_lock.release()
        self.__full_slots.release()
        

    def remove(self):
        self.__full_slots.acquire()
        self.__mutex_lock.acquire()
        url = self.__frontier_queue[self.__read_idx]
        self.__read_idx = (self.__read_idx + 1) % self.__size
        self.__mutex_lock.release()
        self.__empty_slots.release()
        return (url)

 
=======
class SemaphporeCrawlers:
    def semaphore_frontier():
        print("SemaphoreLock")
>>>>>>> bb66df4aee7981379f5f73f3a349e0357f130616
