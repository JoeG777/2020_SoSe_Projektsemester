import sklearn
from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import pickle
#import logWriter
from data_pipeline.daten_klassifizieren.config import classification_config as config


# TODO: logWriter noch einbinden


def load_classifier(classification_config):
    '''Name in Dokumentation: klassifizierer_laden
    Parameter:
        classification_config (dictionary): Konfigurationsdatei mit benoetigten Parametern

    Returns:
        sklearn object: Ein Klassifizierungsalgorithmus aus dem sklearn Paket'''
    new_classifier_method = classification_config["new_classifier_method"]
    if new_classifier_method != "":
        print('a')
        exec_string = classification_config["classification_method_options"][new_classifier_method]
        return eval(exec_string)

    datasource_classifier = classification_config["datasource_classifier"]
    print('b')
    classifier_dictionary = load_dictionary(datasource_classifier)
    print('c')
    event = classification_config["selected_event"]
    classifier = classifier_dictionary[event]
    if classifier == "":
        return sklearn.svm.SVC()
    else:
        return classifier_dictionary[event]
    # TODO: welche klassifizierungsmethode soll genommen werden, wenn beim laden in dem dictionary kein klassifizierer
    #  vorhanden ist


def persist_classifier(classifier, classification_config):
    '''Name in Dokumentation: klassifizierer_persistieren
    Parameter:
        classifier (sklearn object): Ein Klassifizierungsalgorithmus aus dem sklearn Paket
        classification_config (dictionary): Konfigurationsdatei mit benoetigten Parametern

    Returns:
          int: Statuscode, der angibt ob Perstistierung erfolgreich war(0 Erfolg, 1 Misserfolg)'''
    if not isinstance(classifier, sklearn.svm.SVC):
        print()
        #raise ModelPersistorException
        # TODO: exception noch einbinden
    event = classification_config["selected_event"]
    datasource_classifier = classification_config["datasource_classifier"]
    classifier_dictionary = load_dictionary(datasource_classifier)
    classifier_dictionary[event] = classifier
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


