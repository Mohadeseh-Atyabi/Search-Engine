# Search-Engine

In this project, we want to create a search engine for retrieving text documents in such a way that the user enters his query and represents the system of related documents.This project is defined in two phases. 

## The first phase
In this phase of the project, in order to create a simple information retrieval model, it is necessary to index the documents so that when the query is received, the positional index can be used to retrieve related documents. In short, the things to be done in this phase are as follows.
- Data preprocessing
- Creating a spatial index
- Answering the user's question

In the following, each item is explained in full.

### 1- Document preprocessing

Before creating the positional index, it is necessary to preprocess the texts. The necessary steps in this section are as follows.
- Token extraction
- Text normalization
- Remove stop words
- Stemming

To perform the necessary preprocessing, you can choose and use one of the ready-made libraries at your own discretion (Guide: [Library 1](https://github.com/ICTRC/Parsivar) and [Library 2](https://github.com/roshan-research/hazm)) or have your own implementation. Here I used Library 1 (hazm).

### 2- Creating a positional index

Build the positional index using the preprocessed documents in the previous step. In addition to the location of the words in the documents, in the created positional index, it should be known for each word from the dictionary how many times that word is repeated in all the documents. It should also be clear how many times a specific word is repeated in each document. To implement this part, you can choose a suitable data structure at your discretion. (Make sure that the selected data structure is not such that it slows down the model during search and other operations.)

### 3- Answering the user's query

In this section, the user's query is received in the form of a free text. The minimum operators that can be used in this section are "!" as the NOT operator and "" to define an expression. After retreiving, display the documents as ranked. For document ranking, a document containing more query words is more relevant.

### 4- Data set

The dataset used in this project is a collection of news retrieved from several Persian news websites, which will be provided to you in the form of a JSON file. You need to process only "content" as document content. Consider the number of each news as the ID of that document (news) and display the title of the news and the URL of the retrieved document when answering the question so that it is possible to check the correctness of the system.


## The second phase

At this stage, we want to expand the information retrieval model and represent the documents in vector form so that we can rank the search results based on their relevance to the user's query. In this way, a numerical vector is extracted for each document, which is the representation of that document in the vector space, and these vectors are stored. At the time of receiving the query, first the vector corresponding to that query is created in the same vector space and then using a suitable similarity measure, the similarity of the numerical vector of the query with the vector of all documents in the vector space is calculated and finally the output results are sorted based on the degree of similarity. To increase the response speed of the information retrieval model, various methods can be used, which are described in detail below.

### 1- Modeling documents in vector space

In the previous step, after extracting the tokens, the information was stored in the form of a dictionary and a positional index. In this section, the aim is to represent the documents in the vector space. Using the tf-idf weighting method, a numerical vector will be calculated for each document, and finally each document will be represented as a vector containing the weights of all the words of that document. The weight of each word t in a document d, having the document set D, is calculated using the following equation:
```
𝑡𝑓-𝑖𝑑𝑓(𝑡, 𝑑,𝐷) = 𝑡𝑓(𝑡, 𝑑) × 𝑖𝑑𝑓(𝑡,𝐷) = (1 + log(𝑓𝑡,𝑑)) × log(𝑁/𝑛𝑡)
```
In the above vector representation, zero weight is considered for a word that is not in a document, and therefore many elements of the calculated vectors will be zero. To save memory, instead of having a full numeric vector for each document, many of whose elements are zero, you can store the weight of words in different documents in the same lists of posts. At the time of answering the user's question, which is explained below, you can also retrieve the weight of the words in different documents at the same time as searching for words in the lists of posts, and in this way, only the non-zero elements of the document vectors are stored and processed.

### 2- Answering the question in vector space

Having the user's query, extract the vector specific to the query (calculate the weight of the words in the query). Then, using the similarity measure, try to find the documents that have the most similarity (the least distance) to the input query. Then the results display in order of similarity. Different distance criteria can be considered for this task, the simplest of which is cosine similarity between vectors, which calculates the angle between two vectors. This criterion is defined as follows:

![image](https://user-images.githubusercontent.com/72689599/218247060-00c47e84-b608-4438-a75b-8f7769ab7617.png)

### 3- Increasing the speed of query processing
By using the index elimination technique, the problem of high time in the previous step is solved to some extent, but the response time is still not acceptable for many applications. In order to increase the speed of processing and response, you can use Champion lists that before a question is raised and during the document processing stage, a list of the most relevant documents related to each term is kept in a separate list. To implement this section, after building the positional inverted index, create Champion lists and compare only the query vector with the vector of documents obtained by searching in Champion lists and display K related documents.

## Notes
The result of search is returned in query function. Pay attention that if you return ***dictionary_temp***, the first phase is implemented. To run second phase you can return ***sim*** in this function. Feel free to change the return parameter to run different phases of the project :)
