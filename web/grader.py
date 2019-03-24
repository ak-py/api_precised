import numpy as np
import pickle
from pprint import pprint, pformat

valid_ID = set(['101', '102', '103', '104', '105',
                '106', '107', '108', '109', '110', '111'])


def get_benchmark(tykid, predicted_vector, app=None):

    app.logger.debug("get_benchmark")

    type_101 = [1, 1, 1, 0, 0, 0]
    type_102 = [0, 0, 0, 1, 1, 1]
    type_103 = [1, 0]
    type_104 = [0, 1]
    type_108 = [1, 0]
    type_112 = [1, 1, 0, 0]

    tykid_map = {
        101: type_101,
        102: type_102,
        103: type_103,
        104: type_104,
        105: type_101,
        106: type_101,
        107: type_101,
        108: type_108,
        109: type_108,
        110: type_108,
        111: type_108,
        112: type_112,
        113: type_112
    }

    if not tykid:
        app.logger.error('NULL tykid')
        return
    if (int(tykid) not in tykid_map):
        app.logger.error('Invalid tykid. Enter tykid 101-111')
        return

    benchmark_array = tykid_map[int(tykid)]
    app.logger.debug(benchmark_array)

    if len(benchmark_array) != len(predicted_vector):
        app.logger.error('SIZE MISMATCH - benchmark and predicted vector')
        return

    benchmark_vector = np.asarray(benchmark_array)
    app.logger.debug(benchmark_vector)

    return benchmark_vector


def get_path(tykid, app=None):

    if tykid not in valid_ID:
        if app:
            app.logger.warning('Invalid TYK ID -> Loading model 101 (default)')
        else:
            print('Invalid TYK ID -> Loading model 101 (default)')
        classifier_ID = '101'
    else:
        classifier_ID = tykid

    data_path = 'data/'
    pickle_file_path = '/classifier.pickle'
    path = data_path + classifier_ID + pickle_file_path
    if app:
        app.logger.debug('prediction model: '+path)
    else:
        print('prediction model: '+path)

    return path


def channel_grader(tykid, response_text_list, index2word_set, WORDS, app=None):

    file_path = get_path(tykid, app)
    _file = open(file_path, 'rb')
    classifer = pickle.load(_file)
    _file.close()

    from word_feature_vecs import getAvgFeatureVecs

    response = np.asarray(response_text_list)
    response_vectors = getAvgFeatureVecs(
        response, index2word_set, WORDS, 300, app)
    predicted = classifer.predict(response_vectors)

    if app:
        app.logger.debug('predicted: '+pformat(predicted))
    else:
        print('predicted: '+pformat(predicted))

    benchmark = get_benchmark(tykid, predicted, app)

    if app:
        app.logger.debug('benchmark: '+pformat(benchmark))
    else:
        print('benchmark: '+pformat(benchmark))

    scores = (predicted == benchmark)

    if tykid in valid_ID:
        for i, _ in enumerate(scores):
            if not scores[i]:
                scores[i] = True
                app.logger.debug('grace score given on index: '+pformat(i))
                break

    if tykid in ['101', '102', '105', '106', '107']:
        for i, _ in enumerate(scores):
            if not scores[i]:
                scores[i] = True
                app.logger.debug('grace score given on index: '+pformat(i))
                break

    score_total = np.sum(scores*1)

    if app:
        app.logger.debug('scores: '+pformat(scores))
    else:
        print('scores: '+pformat(scores))

    if app:
        app.logger.debug('score_total: '+pformat(score_total))
    else:
        print('score_total: '+pformat(score_total))

    return {'scores': scores.tolist(), 'score_total': int(score_total)}
