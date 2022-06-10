"""
Routine for parsing input from provided URL files
"""
from audioop import reverse
import os
import sys
import csv
import statistics

def parse_url_file(file_path):
    if not os.path.isfile(file_path):
        print("URL Test file '%s' doesn't exist.", file_path)
        return None

    try:
        with open(file_path) as f:
        # with open(file_path, "r", newline="\n") as f:
            data_points = f.readlines()
    except IOError:
        print("Exception while reading URL Test file '%s'. Terminating.", file_path)
        sys.exit(0)

    data_point_list = []
    for value in data_points:
        data_point_list.append(str(value).strip())

    return data_point_list



def get_file_path(folder,file):
    #main.py
    absolutepath = os.path.abspath(__file__)

    #source code file
    fileDirectory = os.path.dirname(absolutepath)

    #Path of parent directory
    # Techniques to implement web crawler
    parentDirectory = os.path.dirname(fileDirectory)

    #Navigate to folder directory
    newPath = os.path.join(parentDirectory, folder)   
    
    if not os.path.exists(newPath):
        os.makedirs(newPath)

    #Navigate to file
    if file:
        newPath = os.path.join(newPath, file)       
    return(newPath)


def create_output_csv_file(filename, foldername = 'Output', header=[], rows =[]):
    """
    Writes results to CSV file.
    """
    output_file = get_file_path(file= filename, folder= foldername)  
    with open(output_file, "a", encoding='UTF8') as output:
        
        writer = csv.writer(output, lineterminator='\n')
        
        # write the header
        if header:
            writer.writerow( header )
        # write the data
        for row in rows:
            writer.writerow(row)



def read_csv_file(filename):
    """
    Reads CSV file.
    """    
    rows = []
    output_file = get_file_path(file= filename, folder='Output')    
    with open(output_file, 'r',  encoding='UTF8') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
        return header, rows

        
def read_logs_file(filename, lock_name):
    header, logs = read_csv_file( filename= filename)
    x_num_threads =[]
    y_num_links = []
    lock_idx = 2
    thread_idx = 3
    links_idx = 4
    #get column number of Lock Option
    for i in range(len(header)):
        if header[i] == "Lock Option":
            lock_idx = i
        elif header[i] == "Number of Threads":
            thread_idx = i
        elif header[i] == "No. of Links Visited":
            links_idx = i

    #read logs of current lock
    thread_links_dict = dict()
    temp = list()
    for col in logs:
        if ( not col ) or ( not col[0] ):
            continue
        count_threads = int(col[thread_idx])
        count_links = int(col[links_idx])
        if col[lock_idx] == lock_name: 
            if count_threads not in thread_links_dict:
                thread_links_dict[count_threads] = list()
            temp = thread_links_dict[count_threads]
            temp.append(count_links)
    for thread_count in sorted(thread_links_dict):        
        x_num_threads.append(thread_count)
        y_num_links.append(int(statistics.mean(thread_links_dict[thread_count])))


    return x_num_threads, y_num_links