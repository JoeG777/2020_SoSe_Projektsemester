import pickle
import os
from data_pipeline.exception.exceptions import PersistorException

FILE_NAME= "current_model.p"
PATH = os.path.dirname(__file__)


def load():
    '''
    Name in documentation: 'laden'
    :return
    '''
    try:
        current_model = pickle.load(open(os.path.join(PATH, FILE_NAME), "rb"))
    except Exception as ex:
        # should log the actual exception here --> repr(ex)
        raise PersistorException('Error while loading current_model: ' + ex.__class__.__name__)

    return current_model


def save(all_prediction_models):
    '''
    Name in documentation: 'speichern'
    :param all_prediction_models:
    :return:
    '''
    try:
        pickle.dump(all_prediction_models, open(os.path.join(PATH, FILE_NAME), "wb"))
    except Exception as ex:
        # should log the actual exception here --> repr(ex)
        raise PersistorException('Error while save current_model.p: ' + ex.__class__.__name__)
