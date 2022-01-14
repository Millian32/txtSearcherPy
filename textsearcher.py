import pathlib
from typing import List
import re
from os.path import exists


class TextSearcher:
    def __init__(self, filename: str):
        # set up initial data structures
        # bail if the file does not exist
        is_file_present = exists(filename)
        if not is_file_present:
            print("Please double check a valid file exists in: " + filename)
            self.data = None
            return

        # clean leading and trailing spaces replace double space for split
        self.data = pathlib.Path(filename).read_text().strip()
        self.data = self.data.replace('  ', ' |')
        self.data = self.data.replace('\n', ' /n')

        self.array_of_data = self.data.split(' ')

        for s in range(len(self.array_of_data)):
            self.array_of_data[s] = self.array_of_data[s].replace('|', '  ')
            self.array_of_data[s] = self.array_of_data[s].replace('/n', '\n').lstrip(' ')

        # set overall bounds
        if len(self.array_of_data) > 0:
            self.array_of_data_start_idx = 0
            self.array_of_data_end_idx = len(self.array_of_data)

    def search(self, query_word: str, context_count: int) -> List[str]:
        # return a list of the match contexts
        hits = []

        # grab a count of the word
        total_word_count = self.data.count(query_word)

        # buck out if the word isn't present
        if total_word_count == 0:
            print(" search word not found ")
            return hits

        # use regex to match word
        rx = re.compile(r'(?<![^\W_]){}(?![^\W_])'.format(re.escape(query_word)), re.I)

        for s in range(len(self.array_of_data)):
            if bool(rx.search(self.array_of_data[s])):
                # calculate starting and ending indexes for phrases returned with matches
                found_word_idx = s
                start_phrase_idx = found_word_idx - context_count
                if start_phrase_idx < 0:
                    start_phrase_idx = 0

                end_phrase_idx = found_word_idx + context_count + 1
                if end_phrase_idx > self.array_of_data_end_idx:
                    end_phrase_idx = self.array_of_data_end_idx

                phrase_array = self.array_of_data[start_phrase_idx: end_phrase_idx]
                phrase = ' '.join([str(n) for n in phrase_array])
                phrase = phrase.replace('.   ', '.  ')

                hits.append(phrase)
                # exit loop if we know we have hit all matches
                if len(hits) == total_word_count:
                    break

        return hits
