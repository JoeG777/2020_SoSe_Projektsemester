import pickle
import os
from data_pipeline.exception.exceptions import PersistorException

FILE_NAME= "current_model.p"
PATH = os.path.dirname(__file__)


def load():
    """
    Name in documentation: 'laden'
    This method is used to load the persisted dictionary all_prediction_models containing the prediction_models,
    their respective scores and the configuration.
    :raises PersistorException - if there is any error with loading the model
    :return all_prediction_models dictionary
    """
    try:
        current_model = pickle.load(open(os.path.join(PATH, FILE_NAME), "rb"))
    except Exception as ex:
        # should log the actual exception here --> repr(ex)
        raise PersistorException('Error while loading current_model: ' + ex.__class__.__name__)

    return current_model


def save(all_prediction_models):
    """
    Name in documentation: 'speichern'
    This method is used to save the dictionary all_prediction_models containing the prediction_models,
    their respective scores and the configuration.
    :param all_prediction_models: the prediction model dictionary to be saved
    :raises PersistorException - if there is any error with saving the models
    """
    try:
        pickle.dump(all_prediction_models, open(os.path.join(PATH, FILE_NAME), "wb"))
    except Exception as ex:
        # should log the actual exception here --> repr(ex)
        raise PersistorException('Error while save current_model.p: ' + ex.__class__.__name__)
