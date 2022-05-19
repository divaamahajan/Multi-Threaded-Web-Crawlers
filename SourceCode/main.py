import file_parser
import validators
import textprint
import requests
from MultiThreadedCrawler import MultiThreadedCrawler 
import os

try:
    LOG_FILENAME = "data_logs.csv"
    
    URL_file = file_parser.get_file_path('TestFiles','TestURL.txt')
    print('Testing data file: \n',URL_file)
    raw_URL_list = file_parser.parse_url_file(URL_file)
    Seed_URL_list  = []
    results = []

    #Validate URL
    for idx,url in enumerate(raw_URL_list):
        if not validators.url(url)  or  requests.get(url=url, timeout=30).status_code != 200:
            print(f"Invalid URL : {url}")
        else: 
            Seed_URL_list.append(url)

    print(f"\nValid Seed URLs :")
    print(*Seed_URL_list, sep= '\n')

    number_of_threads = input("Please input number (default:4) of Threads required to crawl the given URL's : ")
    if not number_of_threads.isdigit():
        number_of_threads = 4
    else:
        number_of_threads = int(number_of_threads)

    print()
    textprint.print_options()
    lock_type = input("Please enter the type of locks (default:Lockfree) you wish to implement: ")


    metadata_rqd = input("Please type 'Y' if you want to store visited links: ").upper()

    if not lock_type.isdigit():
        lock_type = 1
    else:
        lock_type = int(lock_type)

    while Seed_URL_list:
        url = Seed_URL_list.pop()
        spider = MultiThreadedCrawler(url, number_of_threads , lock_type, metadata_rqd)  
        print(textprint.lock_option_str(spider))  
        spider.run_web_crawler()
        spider.write_output(LOG_FILENAME) 

    textprint.plot_graph(filename=LOG_FILENAME, lock_name=textprint.lock_option_str(spider))
    os._exit(5)
    
except Exception as e:
    print("Crawler finished")
    print("Reason:")
    print(e)
    os._exit(5)

