from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec
import gensim
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


def w2v(app=None):
    if app is not None:
        app.logger.debug("* * * LOADING NLP MODELS * * *")
        app.logger.debug("0%")
        # Load Google's pre-trained Word2Vec model.
        w2v_model = gensim.models.KeyedVectors.load_word2vec_format(
            '/nlp/GoogleNews-vectors-negative300.bin', binary=True, limit=600000)

        # If you don't plan to train the model any further, calling
        # init_sims will make the model much more memory-efficient.
        w2v_model.init_sims(replace=True)
        app.logger.debug("50%")

        model_index2word = w2v_model.index2word
        app.logger.debug("80%")

        w_rank = {}
        for i, word in enumerate(model_index2word):
            w_rank[word] = i
        WORDS = w_rank

        # Index2word is a list that contains the names of the words in
        # the model's vocabulary. Convert it to a set, for speed
        index2word_set = set(model_index2word)
        app.logger.debug("100%")

        return w2v_model, index2word_set, WORDS

    print("* * * LOADING NLP MODELS * * *")
    print("0%")
    # Load Google's pre-trained Word2Vec model.
    w2v_model = gensim.models.KeyedVectors.load_word2vec_format(
        '/nlp/GoogleNews-vectors-negative300.bin', binary=True, limit=600000)

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    w2v_model.init_sims(replace=True)
    print("50%")

    model_index2word = w2v_model.index2word
    print("80%")

    w_rank = {}
    for i, word in enumerate(model_index2word):
        w_rank[word] = i
    WORDS = w_rank

    # Index2word is a list that contains the names of the words in
    # the model's vocabulary. Convert it to a set, for speed
    index2word_set = set(model_index2word)
    print("100%")

    return w2v_model, index2word_set, WORDS
