
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from datetime import datetime
import file_parser
import pandas as pd

def print_options():
    print("You can use the different locking mechanisms")
    print("\t1.Lock Free Crawlers")
    print("\t2.Implementation of locks using Semaphore mutex ")
    print("\t3.Implementation of locks using Monitors")

def current_date_str():
    return datetime.now().strftime("%Y-%d-%m")
    
def current_time_str():
    return datetime.now().strftime("%I.%M.%S%p")

def lock_option_str(op):
    if op.semaphorelock:
        return lock_type_str(2)
    elif op.monitorlock:
        return lock_type_str(3)
    else:
        return lock_type_str(1)

def lock_type_str(lock_type):
    if lock_type == 2:
        return "Semaphorelock"
    elif lock_type == 3:
        return "Monitorlock"
    else:
        return "Lockfree"

def plot_graph(filename, lock_name , frontier_size):
    xdata , ydata = file_parser.read_logs_file(filename=filename, lock_name=lock_name)    
    plt.plot(xdata,ydata)
    plt.title(f'Parallel Webcrawlers with {lock_name} | Frontier Size:{frontier_size}')
    plt.ylabel('No. of Links Visited')# naming the x axis
    plt.xlabel('Number of Threads')# naming the y axis
    plt.show()

def plot_overlay_graph(filename,frontier_size):
    for lck in range(1,4):
        lock_name = lock_type_str(lck)
        xdata , ydata = file_parser.read_logs_file(filename=filename, lock_name=lock_name)
        # Data
        df = pd.DataFrame(
            {'Thread_'+lock_name : xdata, 
            lock_name: ydata}
            )
        plt.plot( 'Thread_'+lock_name, lock_name , data=df, marker='', color= get_colors(lck))
    plt.title(f'Parallel Webcrawlers with different locks | Frontier Size:{frontier_size}')
    plt.ylabel('No. of Links Visited')# naming the x axis
    plt.xlabel('Number of Threads')# naming the y axis
    plt.legend() # show legend
    plt.show()

def get_colors(num):  
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    by_hsv = ((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
    colors_names = [name for hsv, name in by_hsv]
    return colors_names[num]
