import datetime
import os
import re
from collections import defaultdict
from nltk.corpus import stopwords
import pylru
import numpy as np
import ntpath
from timeit import default_timer as timer
import nltk


class Search:
    def __init__(self):
        nltk.download('stopwords')
        self.inverted_index = defaultdict(list)
        self.index_created = False
        self.cache_size = 100
        self.lru_cache = pylru.lrucache(self.cache_size)

    def get_dirfiles(self):

        # List all subdirectories using os.listdir
        filenames = list()
        basepath = 'sample_text'
        for entry in os.listdir(basepath):

            if os.path.isfile(os.path.join(basepath, entry)):
                file_name = os.path.join(basepath, entry)
                filenames.append(file_name)
        return filenames

    def string_search(self, query_string):

        if query_string in self.lru_cache:
            return self.lru_cache[query_string]

        fnames = self.get_dirfiles()
        search_results = []

        # traversing files for the required query term
        for file_loc in fnames:
            f = open(file_loc, "r", encoding='utf-8')
            txt = f.read()
            f.close()
            txt = txt.lower()
            query_hits = txt.count(query_string)
            if query_hits > 0:
                search_results.append((file_loc, query_hits))
        search_results.sort(key=lambda x: x[1], reverse=True)

        # Update lru cache
        self.lru_cache[query_string] = search_results

        for index, result in enumerate(search_results):
            head, tail = ntpath.split(result[0])
            search_results[index] = (tail or ntpath.basename(head), result[1])

        return search_results

    def regex_search(self, query_string):
        fnames = self.get_dirfiles()

        exact_results = list()
        imperfect_results = list()

        search_regex = re.compile(r'\w*{0}\w*'.format(query_string), re.I)
        exact_regex = re.compile(r"\b{0}\b".format(query_string), re.I)

        # traversing files for the required query term
        for file_loc in fnames:
            f = open(file_loc, "r",encoding='utf-8')
            txt = f.read()
            f.close()

            query_hits = search_regex.findall(txt)
            exact_query_hits = list()

            for term in query_hits:
                if exact_regex.match(term):
                    exact_query_hits.append(term)

            # getting the filename
            head, tail = ntpath.split(file_loc)
            document_name = tail or ntpath.basename(head)

            if len(exact_query_hits) > 0:
                exact_results.append((document_name, len(exact_query_hits)))

            remaining_term_count = len(query_hits) - len(exact_query_hits)
            if remaining_term_count > 0:
                imperfect_results.append((document_name, remaining_term_count))

        exact_results.sort(key=lambda x: x[1], reverse=True)
        imperfect_results.sort(key=lambda x: x[1], reverse=True)

        return exact_results, imperfect_results

    def index_search(self, query_string):

        if self.index_created:
            return self.inverted_index[query_string]

        stop_words = stopwords.words('english')
        fnames = self.get_dirfiles()

        # traversing files for the required query term
        for file_loc in fnames:
            f = open(file_loc, "r",encoding='utf-8')
            txt = f.read()
            f.close()

            # convert to lower case
            txt = txt.lower()

            # remove references won.[4] --> won.
            txt = re.sub(r'\[\d+\]', '', txt)

            # tokenize
            words = txt.split()

            # remove symbols
            symbols = "!\"#$%&()*+./:;<=>?@[\]^_`{|}~\n"
            for i in range(len(symbols)):
                txt = np.char.replace(txt, symbols[i], '')
                txt = np.char.replace(txt, "  ", " ")
            txt = np.char.replace(txt, ',', '')

            # remove apostrophe
            txt = np.char.replace(txt, "\'", '')

            # remove stop words
            final_word_list = list()
            for w in words:
                if w not in stop_words and len(w) > 1:
                    final_word_list.append(w)

            # fill up the index
            for i in final_word_list:
                if i not in self.inverted_index:
                    self.inverted_index[i] += self.string_search(i)
            self.index_created = True

        return self.inverted_index[query_string]


if __name__ == '__main__':
    s = Search()

    search_term = input("Enter the search term: ")
    search_type = input("Enter search type: \n \"1\" for String Search \n \"2\" Regex search \n \"3\" Indexed search "
                        "\n")

    if search_type == "1":

        start = timer()
        results = s.string_search(search_term)
        end = timer()
        time_diff = (end - start)

        print("Search results:\n")
        if len(results) > 0:
            for result in results:
                print(result[0]," - ", result[1], "\n")
        else:
            print("No document found with search term")

        print("Time elapsed", time_diff,"s")

    elif search_type == "2":
        start = timer()
        exact_results, imperfect_results = s.regex_search(search_term)
        end = timer()
        time_diff = (end - start)

        print("Search results\n")
        if len(exact_results) > 0 or len(imperfect_results) > 0:
            for result in exact_results:
                print("Exact matches:\n")
                print(result[0], " - ", result[1], "\n")
            for result in imperfect_results:
                print("Other matches:\n")
                print(result[0], " - ", result[1], "\n")
        else:
            print("No document found with search term")

        print("Time elapsed", time_diff, "s")

    elif search_type == "3":
        start = timer()
        results = s.inverted_index(search_term)
        end = timer()
        time_diff = (end - start)

        print("Search results:\n")
        if len(results) > 0:
            for result in results:
                print(result[0], " - ", result[1], "\n")
        else:
            print("No document found with search term")

        print("Time elapsed", time_diff, "s")
