import sklearn
from sklearn import *
import pickle
# import logWriter
import data_pipeline.exception.exceptions as ex


# TODO: logWriter noch einbinden
# TODO: model.txt muss existieren und darf nicht leer sein
def load_classifier(classification_config, current_model_type):
    """
    Name in documentation: 'klassifizierer_laden'

    This method loads either an existing model for a specific event or creates an entirely new one from a specified
    algorithm

    :raises ConfigTypeException: Raised if configuration not of type 'dict'
    :raises InvalidConfigKeyException: Raised if a key in the config does not exist
    :raises InvalidConfigValueException: Raised if a value inside of the config is wrong

    :param classification_config: provided by the API
    :return: a trained or untrained model from the sklearn-classification package
    """

    if not isinstance(classification_config, dict):
        raise ex.ConfigTypeException("Wrong data structure of configuration: " + str(classification_config))

    try:
        create_new_classifier, datasource_classifier, event = get_config_parameter(classification_config)
        if create_new_classifier == "True":
            return sklearn.neighbors.KNeighborsClassifier()
            #return sklearn.svm.SVC()
    except KeyError:
        raise ex.InvalidConfigKeyException("No Key found in configuration ")#evtl. genauere aufteilung der Exception notwendig

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        raise ex.InvalidConfigValueException("Wrong configuration values for loading")

    if current_model_type in classifier_dictionary.keys():
        model = classifier_dictionary[current_model_type]
    else:
        raise ex.InvalidConfigKeyException("No such key for event: " + str(current_model_type))

    if model == '':
        return sklearn.neighbors.KNeighborsClassifier()  # TODO: hardcoden oder noch entscheiden durch Analyse
    else:
        return model


def persist_classifier(classifier, classification_config, current_model_type):
    """
    name in documentation: 'klassifizierer_persistieren'

    This method takes a trained or newly created classifier an writes it into the according dictionary which is
    pickled subsequently.

    :param classifier:(sklearn-object) a classification algorithm form the sklearn package
    :param classification_config: configuration file with required parameters

    :raises ConfigTypeException: Raised if configuration not of type 'dict'
    :raises InvalidConfigKeyException: Raised if a key in the config does not exist
    :raises InvalidConfigValueException: Raised if a value inside of the config is wrong
    :raises PersistorException: Raised if classifier is not an instance of sklearn
    :return int: Statuscode, der angibt ob Perstistierung erfolgreich war(0 Erfolg, 1 Misserfolg)
    """

    if not isinstance(classification_config, dict):
        raise ex.ConfigTypeException("Wrong data structure of configuration: " + str(classification_config))

    try:
        create_new_classifier, datasource_classifier, event = get_config_parameter(classification_config)
    except KeyError:
        raise ex.InvalidConfigKeyException("Wrong key for Configuration")

    if not (isinstance(classifier, sklearn.svm.SVC) | isinstance(classifier, sklearn.neighbors._classification.KNeighborsClassifier)):
        raise ex.PersistorException("Not a valid classification model")

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        raise ex.InvalidConfigValueException("Wrong configuration values for loading")

    if current_model_type in classifier_dictionary.keys():
        classifier_dictionary[current_model_type] = classifier
    else:
        raise ex.InvalidConfigKeyException("No such key for event: " + str(current_model_type))

    save_dictionary(classifier_dictionary, datasource_classifier)
    return 0


def load_dictionary(datasource_classifier):
    """
    Loads the dictionary containing all the available classifcation-models for the events with pickle.

    :raises InvalidConfigValueException: Raised when there is nothing to unpickle e.g. the file is empty
    :param datasource_classifier: the file in which the dictionary is currently stored
    :return dictionary: unpickled dictionary {"event_name": sklearn-model}
    """
    if datasource_classifier == "" or datasource_classifier is None:
        raise ex.InvalidConfigValueException("Empty value: 'datasource_classifier")

    with open(datasource_classifier, "rb") as file:
        try:
            content = pickle.load(file)
        except pickle.UnpicklingError:
            raise ex.InvalidConfigValueException("No content in the specified file: " + str(datasource_classifier))
        except IOError:
            raise ex.FileException("The specified file is not accessible: " + str(datasource_classifier))

    return content


def save_dictionary(classifier_dictionary, datasource_classifier):
    """
     Saves the dictionary containing all the available classifcation-models for the events with pickle.

    :param classifier_dictionary: dictionary {"event_name": sklearn-model}
    :param datasource_classifier: the file in which the dictionary should be stored
    :return:
    """
    with open(datasource_classifier, "wb") as file:
        pickle.dump(classifier_dictionary, file)


def get_config_parameter(config):
    """
    Returns the needed parameters in this file contained in the configuration

    :param config: dictionary of all required parameters
    :return new_classifier_method:
    :return datasource_classifier: the file in which the dictionary ist currently stored
    :return event: happening which should be detected by the classifier
    """
    create_new_classifier = config["create_new_classifier"]
    datasource_classifier = config["datasource_classifier"]
    event = config["selected_event"]
    return create_new_classifier, datasource_classifier, event
