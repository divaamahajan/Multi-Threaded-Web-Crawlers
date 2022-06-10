# import file_parser
import textprint
# import validators
# import requests
from multithreadedcrawler import MultiThreadedCrawler 
import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--EXCEPTION_FILENAME'  , type=str)
parser.add_argument('--FRONTIER_SIZE'       , type= int )
parser.add_argument('--LOG_FILENAME'        , type= str )
parser.add_argument('--seed_url_list'       , type= str)
parser.add_argument('--number_of_threads'   , type= int )
parser.add_argument('--lock_type'           , type= int )
parser.add_argument('--metadata_rqd'        , type= str )


args = vars(parser.parse_args())
print(args)
try:
    EXCEPTION_FILENAME  = args['EXCEPTION_FILENAME'] #arg parser1
    FRONTIER_SIZE       = args['FRONTIER_SIZE'] #arg parser2
    LOG_FILENAME        = args['LOG_FILENAME'] #arg parser3
    seed_url_list       = list(args['seed_url_list'].split(" ,"))#arg parser4
    number_of_threads   = args['number_of_threads'] #arg parser5
    lock_type           = args['lock_type'] #arg parser6
    metadata_rqd        = args['metadata_rqd'] #arg parser7

    # URL_file = file_parser.get_file_path('TestFiles',test_file)
    # print('Testing data file: \n',URL_file)
    # raw_URL_list = file_parser.parse_url_file(URL_file)
    # seed_url_list  = []
    # results = []

    # #Validate URL
    # for idx,url in enumerate(raw_URL_list):
    #     if not validators.url(url)  or  requests.get(url=url, timeout=30).status_code != 200:
    #         print(f"Invalid URL : {url}")
    #     else: 
    #         seed_url_list.append(url)
    # if not seed_url_list:
    #     print(f"No valid URL found. Please update the test file{test_file}")
    #     os.exit(1)
        
    # print(f"\nValid Seed URLs :")
    # print(*seed_url_list, sep= '\n')

    # number_of_threads = input("Please input number (default:4) of Threads required to crawl the given URL's : ")
    # if not number_of_threads.isdigit():
    #     number_of_threads = 4
    # else:
    #     number_of_threads = int(number_of_threads)

    # print()
    # textprint.print_options()
    # lock_type = input("Please enter the type of locks (default:Lockfree) you wish to implement: ")

    # if not lock_type.isdigit():
    #     lock_type = 1
    # else:
    #     lock_type = int(lock_type)

    # metadata_rqd = input("\nPlease type 'Y' if you want to store visited links: ").upper()
    while seed_url_list:
        url = seed_url_list.pop()
        spider = MultiThreadedCrawler(url, number_of_threads , lock_type, metadata_rqd, FRONTIER_SIZE)  
        print(textprint.lock_option_str(spider))  
        spider.run_web_crawler()
        spider.write_output(LOG_FILENAME) 
        spider.write_exceptions(EXCEPTION_FILENAME)

    # textprint.plot_graph(filename=LOG_FILENAME, lock_name=textprint.lock_type_str(lock_type),frontier_size=FRONTIER_SIZE)
    # textprint.plot_overlay_graph(filename=LOG_FILENAME,frontier_size=FRONTIER_SIZE)
    # os._exit(5)
    
except Exception as e:
    print(f"/nCrawler finished /nReason:{e}")
    os._exit(5)

