import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import re
import unicodedata

from word2vec_api import get_word_vector


# ****** Define functions to create average word vectors of paragraphs
def makeFeatureVec(words, index2word_set, num_features=300):
    # Function to average all of the word vectors in a given paragraph
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,), dtype="float32")

    # number of words
    nwords = 0.

    # Loop over each word in the response and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in word_tokenize(words):
        if word in index2word_set:
            nwords = nwords + 1.

            # get word vecotr
            vector = get_word_vector(word)

            featureVec = np.add(featureVec, vector)

    # edge case handling
    if (nwords < 1):
        nwords = 1

    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec, nwords)
    return featureVec


def getAvgFeatureVecs(reviews, index2word_set, WORDS, num_features=300, app=None):
    '''Given a set of reviews (each one a list of words), calculate the average feature vector for each one and return a 2D numpy array'''

    lemma = nltk.wordnet.WordNetLemmatizer()

    blacklist = ['/', '@', '"', ':', '!', ';', '.', ',', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the']
    blacklist_set = set(blacklist)

    # a table structure to hold the different punctuation used
    tbl = dict.fromkeys(i for i in range(
        65535) if unicodedata.category(chr(i)).startswith('P'))

    def remove_punctuation(text):
        '''method to remove punctuations from sentences'''
        return text.translate(tbl)

    def words(text):
        return re.findall(r'\w+', text.lower())

    def P(word):
        "Probability of `word`."
        # use inverse of rank as proxy
        # returns 0 if the word isn't in the dictionary
        return - WORDS.get(word, 0)

    def correction(word):
        "Most probable spelling correction for word."
        return max(candidates(word), key=P)

    def candidates(word):
        "Generate possible spelling corrections for word."
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

    def known(words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)

    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    def clean_review(review):
        '''clean the given reveiw'''

        review = remove_punctuation(review)
        splits = review.split()
        cleaned = []
        for single_word in splits:
            if single_word not in blacklist_set:
                cleaned.append(correction(
                    lemma.lemmatize(single_word.lower())))
        return ' '.join(cleaned)

    # Initialize a counter
    counter = 0.

    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews), num_features), dtype="float32")

    # Loop through the samples
    for review in reviews:

        cleaned_review = clean_review(review)

        if app:
            app.logger.debug(cleaned_review)
        else:
            pass

        # Call the function (defined above) that makes average feature vectors
        reviewFeatureVecs[int(counter)] = makeFeatureVec(
            cleaned_review, index2word_set, num_features)

        # Increment the counter
        counter = counter + 1.

    return reviewFeatureVecs
