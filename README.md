# Search-Engine

This project is defined in two phases. In this project, we want to create a search engine for retrieving text documents in such a way that the user enters his query and represents the system of related documents.

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

To perform the necessary preprocessing, you can choose and use one of the ready-made libraries at your own discretion (Guide: [Library 1](https://github.com/ICTRC/Parsivar) and [Library 2](https://github.com/roshan-research/hazm)) or have your own implementation.
