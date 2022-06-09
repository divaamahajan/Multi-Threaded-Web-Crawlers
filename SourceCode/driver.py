import subprocess
import os
from subprocess import Popen
import file_parser
import validators
import requests
import textprint as text

EXCEPTION_FILENAME = 'exceptions.csv'
FRONTIER_SIZE = 10
LOG_FILENAME = f"data_log_frontier{FRONTIER_SIZE}_{text.current_date_str}.csv"
def validate_url(test_file):
    seed_url_list  = []
    try:
        #get file data
        URL_file = file_parser.get_file_path('TestFiles',test_file)
        print('Testing data file: \n',URL_file)
        raw_URL_list = file_parser.parse_url_file(URL_file)
        
        #Validate URL
        for url in raw_URL_list:
            try:
                if not validators.url(url)  or  requests.get(url=url, timeout=30).status_code != 200:
                    print(f"Invalid URL : {url}")
                else: 
                    seed_url_list.append(url)
            except Exception as e:
                print(e)
                continue
        if not seed_url_list:
            print(f"No valid URL found. Please update the test file{test_file}")
            print('terminating...')
            os.exit(1)
    except Exception as e:
        print(f'Input file exception caught : {e}')
        return
        
    print(f"\nValid Seed URLs :")
    print(*seed_url_list, sep= '\n')
    return seed_url_list

def get_seed_url_list():
    text.local_server_intro()
    test_file = input('Would you like test on \n\t1. Local Server(default) ..TestFiles\TestURL_local_server.txt \n\t2. updated ..TestFiles\TestURL.txt')
    if test_file == '2':
        test_file = 'TestURL.txt'
    else:
        test_file = 'TestURL_local_server.txt'
    return validate_url(test_file=test_file)

def get_max_threads():
    max_threads = input("Please input maximum number (default:4) of Threads required to crawl the given URLs : ")
    if not max_threads.isdigit():
        max_threads = 4
    else:
        max_threads = int(max_threads)

def get_lock_type():
    lock_type = input("Please enter the type of lock (default: 1.Lockfree) you wish to implement from above options: ")
    if not lock_type.isdigit():
        lock_type = 1
    else:
        lock_type = int(lock_type)
    return lock_type

def start_fastapiserver():
    print('initializing Fast API server...')
    return p

def kill_fastapiserver(p):
    p.terminate()


try:
    start_path = file_parser.get_file_path('SourceCode','startcrawler.py')   
    max_threads = get_max_threads()
    print()
    text.print_locking_options()
    automate = input(f'Would you like to automate the WebCrawler to run up to 1 to {max_threads} threads for all available locks respectively(Y/N) : ')
    if automate.upper() == 'Y':
        automate = True    
    else:
        automate = False
        lock_type = get_lock_type()
    metadata_rqd = input("\nPlease type 'Y' if you want to store the list of visited links: ").upper()
    seed_url_list = get_seed_url_list()
except Exception as e:
    print(f'Input Error caught : {e} \nterminating...')
    os._exit(1)

try:
    if not automate:
        p = start_fastapiserver()
        subprocess.call( start_path , 
                        EXCEPTION_FILENAME,
                        FRONTIER_SIZE,
                        LOG_FILENAME,
                        seed_url_list ,
                        max_threads,
                        lock_type ,
                        metadata_rqd )
        kill_fastapiserver(p)
        try:
            text.plot_graph(filename=LOG_FILENAME, lock_name=text.lock_type_str(lock_type),frontier_size=FRONTIER_SIZE)
        except Exception as e:
            print(f'Error caught while plotting the {lock_type} graph: {e} \nterminating...')
            os._exit(5)

    else:
        for t in range (1,max_threads):
            for l in range(9):
                lck = (l%3) +1
                p = start_fastapiserver()
                subprocess.call( start_path , 
                                EXCEPTION_FILENAME,
                                FRONTIER_SIZE,
                                LOG_FILENAME,
                                seed_url_list ,
                                t,
                                lck ,
                                metadata_rqd ) 
                kill_fastapiserver(p)
except Exception as e:
    print(f'Error caught : {e} \nterminating...')

try:
    text.plot_overlay_graph(filename=LOG_FILENAME,frontier_size=FRONTIER_SIZE)
    os._exit(5)
except Exception as e:
    print(f'Error caught while plotting the overlay graph: {e} \nterminating...')
    os._exit(5)

# def get_command_list(cmd):
#     return cmd.split(" ")

# for t in range(50,51 ,2):
#     for l in range(1):
#         lck = (l%3) + 1
        
#         # start fastapiserver
#         os.chdir("/Users/achin.gupta/Documents/exps/fastapi")
        
#         p = Popen(['/Users/achin.gupta/Documents/exps/fastapi/venv/bin/uvicorn', 'app.main:app'])


#         # call webcrawler
#         os.chdir("/Users/achin.gupta/Documents/exps/webcrawler/TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING")

#         subprocess.call(['/Users/achin.gupta/.webcrawler-coder/bin/python3', 
#                          '/Users/achin.gupta/Documents/exps/webcrawler/TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING/SourceCode/main.py', 
#                          "-th", str(t), "-lt", str(lck)])

#         # kill fastapi server
#         p.terminate()