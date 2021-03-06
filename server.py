from flask import Flask
from search import Search
search_api= Flask('server')

s = Search()
@search_api.route('/api/stringsearch', defaults={'query_term': 'france'})
@search_api.route('/api/stringsearch/<query_term>')
def string_search_handler(query_term):
    results = s.string_search(query_term)
    return {
        'query_term': query_term,
        'search_results': results
    }, 200

@search_api.route('/api/regexsearch', defaults={'query_term': 'france'})
@search_api.route('/api/regexsearch/<query_term>')
def regex_search_handler(query_term):
    exact_results, imperfect_results = s.regex_search(query_term)
    return {
        'query_term': query_term,
        'top_search_results': exact_results,
        'other_results': imperfect_results
    }, 200

@search_api.route('/api/indexsearch', defaults={'query_term': 'france'})
@search_api.route('/api/indexsearch/<query_term>')
def index_search_handler(query_term):
    results = s.index_search(query_term)
    return {
        'query_term': query_term,
        'search_results': results
    }, 200


if __name__ == '__main__':
    search_api.run(host='0.0.0.0', port=8080)
