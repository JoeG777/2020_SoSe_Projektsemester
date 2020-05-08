import sklearn
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import pickle
#import logWriter
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex


# TODO: logWriter noch einbinden


def load_classifier(classification_config):
    '''
    Name in documentation: 'klassifizierer_laden'
    This method loads either an existing model for a specifice event or creates an entirely new one from a specified
    algorithm

    :param classification_config: provided by the API

    :raises PersistorException BESCHREIBUNG
    :return sklearn-model: a trained or untrained model from the sklearn-classification package

    '''

    new_classifier_method, datasource_classifier, event = get_config_parameter(classification_config)

    if new_classifier_method != "":
        exec_string = classification_config["classification_method_options"][new_classifier_method]
        return eval(exec_string)

    classifier_dictionary = load_dictionary(datasource_classifier)
    model = classifier_dictionary[event]

    if model == "":
        return sklearn.svm.SVC()  # TODO: hardcoden oder noch entscheiden durch Analyse
    else:
        return model


def persist_classifier(classifier, classification_config):
    '''Name in Dokumentation: klassifizierer_persistieren
    Parameter:
        classifier (sklearn object): Ein Klassifizierungsalgorithmus aus dem sklearn Paket
        classification_config (dictionary): Konfigurationsdatei mit benoetigten Parametern

    Returns:
          int: Statuscode, der angibt ob Perstistierung erfolgreich war(0 Erfolg, 1 Misserfolg)'''
    # TODO: bundle exceptions, implement ModelPersistorException, ConfigError, raise with message
    try:
        new_classifier_method, datasource_classifier, event = get_config_parameter(classification_config)
    except KeyError:
        return "ConfigError"
        # TODO: exception noch einbinden

    if not isinstance(classifier, sklearn.svm.SVC):
        return "ModelPersistorException"
        #raise ModelPersistorException
        # TODO: exception noch einbinden

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        return "ConfigError"
        # TODO: Exception: Was passiert bei falscher Source?

    if event in classifier_dictionary.keys():
        classifier_dictionary[event] = classifier
    else:
        return "ConfigError"
    # TODO: Exception einbinden

    save_dictionary(classifier_dictionary, datasource_classifier)
    return 0


def load_dictionary(datasource_classifier):
    '''Name in Dokumentation: -
    Parameter:
        -
    Returns:
        dictionary: Dictionary, das alle Klassifizierer enthaelt'''
    with open(datasource_classifier, "rb") as file:
        return pickle.load(file)


def save_dictionary(classifier_dictionary, datasource_classifier):
    '''Name in Dokumentation: -
    Parameter:
        classifier_dictionary (dictionary): Dictionary, das alle Klassifizierer enthaelt
    Returns:
        -'''
    with open(datasource_classifier, "wb") as file:
        pickle.dump(classifier_dictionary, file)


def get_config_parameter(config):
    new_classifier_method = config["new_classifier_method"]
    datasource_classifier = config["datasource_classifier"]
    event = config["selected_event"]
    return new_classifier_method, datasource_classifier, event
