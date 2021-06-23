import nltk
import sys
import os
import string
import math

FILE_MATCHES = 4
SENTENCE_MATCHES = 1

# Initial setup
nltk.download('punkt')
nltk.download('stopwords')

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = dict()

    for txt_file in os.listdir(directory):

        # Determine the path for each text file
        path = os.path.join(directory, txt_file)
        
        # Accept text files only
        if txt_file.endswith('.txt') and os.path.isfile(path):
            
            # Open file and write its content to the dict
            with open(path, 'r', encoding='utf8') as file:        
                corpus[txt_file] = file.read()

    return corpus


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.
    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenization
    words = nltk.word_tokenize(document)
    
    # STEP 1: Convert incoming words to lowercase
    # STEP 2: Exclude the stopwords
    # STEP 3: Remove all punctuations, except for words CONTAINING punctuation
    return [word.lower() for word in words if not all(char in string.punctuation for char in word) and word not in nltk.corpus.stopwords.words('english')]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Keeps count of a word in all documents
    global_count = dict()

    # Cycle through all text files
    for txt_file in documents:
        past_words = set()

        # Iterate through all words in current text file
        for word in documents[txt_file]:

            # Maintain the past_words set
            if word not in past_words:
                past_words.add(word)

                # Update the global count
                try:
                    global_count[word] += 1
                except KeyError:
                    global_count[word] = 1

    # Return a dict after applying the IDF formula for each word
    return {word: math.log(len(documents) / global_count[word]) for word in global_count}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    for txt_file in files:
        
        # Initialize a value for each file
        tf_idfs[txt_file] = 0
        
        # Find the overall TF-IDF value of the current document by looping through the query
        for word in query:
            tf_idfs[txt_file] += files[txt_file].count(word) * idfs[word]

    # Sort all files in descending order by their TF-IDF values
    # Return the highest-ranking 'n' files
    return [key for key, value in sorted(tf_idfs.items(), key=lambda txt_file: txt_file[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranked_sentences = list()

    # Iterate through all sentences
    for sentence in sentences:
        # Initialize the structure for a sentence's values
        # [sentence, matching word measure, query term density]
        sentence_values = [sentence, 0, 0]

        # Iterate through the query
        for word in query:
            if word in sentences[sentence]:
                
                # Add IDF value of word to sentence's IDF value (matching word measure)
                sentence_values[1] += idfs[word]

                # Recognize the query's term density
                sentence_values[2] += sentences[sentence].count(word) / len(sentences[sentence])

        # Add the calculated values to the sorted list
        ranked_sentences.append(sentence_values)
        
    # Sort all sentences in descending order by their overall TF-IDF values
    # Return the highest-ranking 'n' sentences
    return [sentence for sentence, matching_word_measure, query_term_density in sorted(ranked_sentences, key=lambda sentence: (sentence[1], sentence[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()