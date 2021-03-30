import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from document_search.search import Search



class TestSearch(unittest.TestCase):
    def test_string_search(self):
        test_string = "power"
        s = Search()
        result = s.string_search(test_string)
        files_count = len(result)
        self.assertEqual(1, files_count)
        self.assertEqual('french_armed_forces.txt', result[0][0])
        self.assertEqual(7, result[0][1], "Search match count is wrong")

    def test_regex_search(self):
        test_string = "power"
        s = Search()
        exact_matches, imperfect_matches = s.regex_search(test_string)
        files_count = len(exact_matches)
        self.assertEqual(1, files_count)
        self.assertEqual('french_armed_forces.txt', exact_matches[0][0])
        self.assertEqual(3, exact_matches[0][1], "Exact search match count is wrong")
        self.assertEqual(4, imperfect_matches[0][1], "Other search match count is wrong")

    def test_index_search(self):
        test_string = "power"
        s = Search()
        result = s.index_search(test_string)
        files_count = len(result)
        self.assertEqual(1, files_count)
        self.assertEqual('french_armed_forces.txt', result[0][0])
        self.assertEqual(7, result[0][1], "Search match count is wrong")

    def test_get_file_count(self):
        s = Search()
        file_locs = s.get_dirfiles()
        self.assertEqual(3, len(file_locs), "Failed to read all files from the directory")

    def test_cache_usage(self):
        s = Search()
        print("\nInitial cache length: ",len(s.lru_cache))
        s.string_search("power")
        self.assertEqual(1, len(s.lru_cache), "Cache not storing recently searched term")


if __name__ == '__main__':
    unittest.main()
