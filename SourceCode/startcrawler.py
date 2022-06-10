import textprint
import os
import argparse
from MultiThreadedCrawler import MultiThreadedCrawler
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
    while seed_url_list:
        url = seed_url_list.pop()
        spider = MultiThreadedCrawler(url, number_of_threads , lock_type, metadata_rqd, FRONTIER_SIZE)  
        print(textprint.lock_option_str(spider))  
        spider.run_web_crawler()
        spider.write_output(LOG_FILENAME) 
        spider.write_exceptions(EXCEPTION_FILENAME)
    
except Exception as e:
    print(f"/nCrawler finished /nReason:{e}")
    os._exit(5)

