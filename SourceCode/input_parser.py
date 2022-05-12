"""
Routine for parsing input from provided URL files
"""
import os
import sys

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
    # Aging ALgo
    parentDirectory = os.path.dirname(fileDirectory)

    #Navigate to folder directory
    newPath = os.path.join(parentDirectory, folder)   
    
    if not os.path.exists(newPath):
        os.makedirs(newPath)

    #Navigate to file
    newPath = os.path.join(newPath, file)       
    return(newPath)
