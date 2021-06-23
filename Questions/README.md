
# ❓ Questions Project

**Objective:** Write an AI to answer questions.

## 📺 Demonstration

```
$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
```

## 🌉 Background

Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. Among the more famous question answering systems is  [Watson](https://en.wikipedia.org/wiki/Watson_(computer)), the IBM computer that competed (and won) on  _Jeopardy!_. A question answering system of Watson’s accuracy requires enormous complexity and vast amounts of data, but in this problem, we design a very simple question answering system based on inverse document frequency.

The question answering system performs two tasks: document retrieval and passage retrieval. It has access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval first identifies which document(s) are most relevant to the query. Once the top documents are found, the top document(s) are subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

How do we find the most relevant documents and passages? To find the most relevant documents, we use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once we’ve found the most relevant documents, there are [many possible metrics](https://groups.csail.mit.edu/infolab/publications/Tellex-etal-SIGIR03.pdf)  for scoring passages, but I’ll use a combination of inverse document frequency and a query term density measure (described in the Specification).

More sophisticated question answering systems might employ other strategies (analyzing the type of question word used, looking for synonyms of query words,  [lemmatizing](https://en.wikipedia.org/wiki/Lemmatisation)  to handle different forms of the same word, etc.)

## 🧐 Understanding

First, take a look at the documents in  `corpus`. Each is a text file containing the contents of a Wikipedia page. Our goal is to write an AI that can find sentences from these files that are relevant to a user’s query. You are welcome and encouraged to add, remove, or modify files in the corpus if you’d like to experiment with answering queries based on a different corpus of documents. Just be sure each file in the corpus is a text file ending in  `.txt`.

Now, take a look at  `questions.py`. The global variable  `FILE_MATCHES`specifies how many files should be matched for any given query. The global variable  `SENTENCES_MATCHES`  specifies how many sentences within those files should be matched for any given query. By default, each of these values is 1: our AI will find the top sentence from the top matching document as the answer to our question. You are welcome and encouraged to experiment with changing these values.

In the  `main`  function, we first load the files from the corpus directory into memory (via the  `load_files`  function). Each of the files is then tokenized (via  `tokenize`) into a list of words, which then allows us to compute inverse document frequency values for each of the words (via  `compute_idfs`). The user is then prompted to enter a query. The  `top_files`  function identifies the files that are the best match for the query. From those files, sentences are extracted, and the  `top_sentences`function identifies the sentences that are the best match for the query.
