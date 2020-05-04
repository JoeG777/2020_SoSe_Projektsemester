import pickle
from data_pipeline.vorhersage_berechnen.prediction_core.exception.prediction_core_exceptions import PersistorException

file_name = "current_model.p"

def load():
    '''
    Name in documentation: 'laden'
    :return
    '''
    current_model = None

    try:
        current_model = pickle.load(open(file_name, "rb"))
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
        pickle.dump(all_prediction_models, open(file_name, "wb"))
    except Exception as ex:
        # should log the actual exception here --> repr(ex)
        raise PersistorException('Error while save current_model.p: ' + ex.__class__.__name__)
