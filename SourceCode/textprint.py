
import matplotlib.pyplot as plt
from datetime import datetime
import file_parser
def print_options():
    print("You can use the different locking mechanisms")
    print("\t1.Lock Free Crawlers")
    print("\t2.Implementation of locks using Semaphore mutex ")
    print("\t3.Implementation of locks using Monitors")

def current_date_str():
    return datetime.now().strftime("%Y-%d-%m")
    
def current_time_str():
    return datetime.now().strftime("%H-%M-%S")

def lock_option_str(op):
    if op.semaphorelock:
        return "Semaphorelock"
    elif op.monitorlock:
        return "Monitorlock"
    else:
        return "Lockfree"

def plot_graph(filename, lock_name):

    xdata , ydata = file_parser.read_logs(filename=filename, lock_name=lock_name)
    
    # plt.bar(range(len(xdata)),ydata)
    plt.plot(xdata,ydata)
    plt.title(lock_name)
    plt.ylabel('No. of Links Visited')# naming the x axis
    plt.xlabel('Number of Threads')# naming the y axis
    plt.show()
