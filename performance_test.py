from search import Search
from timeit import default_timer as timer
from nltk.corpus import words
import nltk
import random

if __name__ == '__main__':
    nltk.download('words')
    word_list= words.words()

    s = Search()

    print("-------Starting performance test-------")
    start = timer()
    for _ in range(2000000):
        word = random.choice(word_list)
        s.string_search(word)
    end = timer()
    time_diff = (end - start)
    print("\nstring_search performance:", time_diff, "s")

    start = timer()
    for _ in range(2000000):
        word = random.choice(word_list)
        s.regex_search(word)
    end = timer()
    time_diff = (end - start)
    print("regex_search performance:", time_diff, "s")

    start = timer()
    for _ in range(2000000):
        word = random.choice(word_list)
        s.index_search(word)
    end = timer()
    time_diff = (end - start)
    print("index_search performance:", time_diff, "s")
