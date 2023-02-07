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

