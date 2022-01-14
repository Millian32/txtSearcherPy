import argparse
import sys
import time
from datetime import datetime
from textsearcher import TextSearcher

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input parsing and search info')
    parser.add_argument('-f', '--file',
                        default='./files/short_excerpt.txt',
                        help="text file to be searched.  place file in files folder in current dir, "
                             "default ex: './files/short_excerpt.txt'")
    parser.add_argument('-c', '--contextcount',
                        default=4,
                        help=' number of additional words to display for context, 0 to 7 please, default  is 3 ')

    args = parser.parse_args()
    search_word = "GO!"

    if len(args.file) < 2:
        time.sleep(3)
        sys.exit('Please check file name entered')

    file_name = args.file
    context_count = int(args.contextcount)

    # this is where the rubber meets the road...
    text_searcher = TextSearcher(file_name)

    # failed to get data from file path provided
    if text_searcher.data is None:
        print('-exiting program-')
        search_word = 'STOP!'
        time.sleep(3)

    while search_word != 'STOP!':
        while context_count < 0 or context_count > 7:
            if context_count < 0 or context_count > 7:
                print(" Please enter a context word count from 0-7 ")
                context_count = int(input())
        print(" Please enter search word, STOP! to quit ")
        search_word = input()

        # metrics can help improve performance!
        print(' start time: ' + str(datetime.now()))
        start_time = time.time()
        returned_hits = text_searcher.search(search_word, context_count)
        end_time = time.time()
        print(' end time: ' + str(datetime.now()))
        print(' total search time: ' + str(end_time - start_time))

        print(returned_hits)
