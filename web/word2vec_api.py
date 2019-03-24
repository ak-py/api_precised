import requests
import base64
import numpy as np
import pickle
import codecs
import pickle

# these methods are used to connect to flask api run by word2vector-api module in another repo


def get_word_vector(word):
    # temp urls for testing
    url = 'http://0.0.0.0:8888/word2vec/model?word=%s' % (word)
    response = requests.get(url)
    encoded = response.text
    decoded = base64.b64decode(encoded)
    vector = np.frombuffer(decoded, dtype=np.float32, count=-1)
    return vector


def get_index2word_set():
    # temp urls for testing
    url = 'http://0.0.0.0:8888/word2vec/model_word_set'
    response = requests.get(url)
    encoded = response.text
    decoded = base64.b64decode(encoded)
    index2word_set = pickle.loads(decoded)
    return index2word_set


def get_word_rank():
    # temp urls for testing
    url = 'http://0.0.0.0:8888/word2vec/model_word_rank'
    response = requests.get(url)
    encoded = response.text
    decoded = base64.b64decode(encoded)
    WORDS = pickle.loads(decoded)
    return WORDS
