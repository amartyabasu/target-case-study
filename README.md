## Table of content

- [Design Details](#design-details)
    - [String Search](#string-search)
    - [Regex Search](#regex-search)
    - [Index Search](#index-search)
- [Running the App](#Running-the-App)
    - [Local execution](#local-execution)
    - [AWS Deployment](#aws-deployment)
- [Performance Analysis](#performance-analysis)
- [Unit Test](#unit-test)
- [Future Enhancements](#future-enhancements)

## Design Details

This is an application to search a term across multiple documents. Three approaches are implemented to provide the search capability with variations to improve performance and enable meaningful word search. The searches ignore letter cases with the thought process that its not required for an e-commerce site's search functionality.

The application services are accessible by rest enabled end-points for easy plug in to the UI client code.
## String Search

The most simplistic approach of all where every document is visited to find the number of occurrences. This search returns a result where the query term may be a substring of a larger word.  

This search is not optimal as every time a user does a search, all documents are traversed to return the relevant ones. Here relevance is defined by the frequency of the word in the documents that contain it.

A LRU cache is included as part of the implementation to speed up responses for frequently searched or recently used terms.

## Regex Search

This feature allows a user to retrieve documents with exact term matches along with other related matches. Currently only the count of the related match is returned as that is the expected behavior defined in the case study. But with simple tweaks even that can be displayed in the output.

This functionality can also accept a user defined regular expression and return count of the matches based on it.

## Index search

This search mechanism precomputes the inverted document frequency along with the term frequency. These pre-computations are held in-memory after the first time its created and then subsequent searches are looked up in it. 

### Running the App

## Local execution

Follow the following steps to run locally on your system:
1. Install python3 (preferably)
2. Clone the repo to a location in your system
3. Start a terminal from inside the cloned repo directory and install dependencies by running
```
pip3 install --user -r requirements.txt
```
4. Execute following command to interact with the terminal interface
```
python3 search.py
```
4. (Optional) Start the flask server by running
```
python3 server.py
```
5. Open a browser and the endpoints will render the search results. The three search capabilities are exposed by the following endpoints
```
localhost:8080/api/stringsearch/<place your search term here>
localhost:8080/api/regexsearch/<place your search term here>
localhost:8080/api/indexsearch/<place your search term here>
```

## AWS Deployment

Follow the following steps to run locally on your system:
1. Configure and start an EC2 instance on AWS.
2. Configure the associated Security Group for the client by adding an inbound rule to include custom TCP traffic for port 8080 with source as 'Anywhere'.
3. Follow the local system setup. The flask server should be started within a TMUX session so that it operates even after the ssh session dies.

### Performance Analysis

The three different approaches were stress tested with 2 million random words. The execution time was noted to guage the rate of search result retrieval.

* string_search performance: 1303.7215265 s
* regex_search performance: 4704.5470226 s
* index_search performance: 5.030461999999716 s

### Unit Test

The test suite for the project can run by running the following command:
```
python3 -m unittest
```

### Future enhancements

* For a real-time scenario it would help to store the inverted index in a persistent storage like database
* Large requests in the order of more than 5000 requests per second can be catered by -
    1. Allocating more RAM that could support a larger cache for frequently searched terms
    2. Running separate thread to update the inverted index as an when new documents arrive in the datastore
    3. Compute the inverted index by running parallel spark jobs on data distributed across multiple nodes
    4. Probabilistically load the next set of documents based on current term to reduce subsequent search time
    5. Gauge network traffic to add and remove more CPUs on the fly to deal with spikes and ebbs