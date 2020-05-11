import sklearn
from sklearn import *
import pickle
#import logWriter
import data_pipeline.exception.exceptions as ex


# TODO: logWriter noch einbinden

def load_classifier(classification_config):
    """
    Name in documentation: 'klassifizierer_laden'

    This method loads either an existing model for a specific event or creates an entirely new one from a specified
    algorithm

    :raises InvalidConfigurationException: Raised if no access or wrong values inside of the configuration

    :param classification_config: provided by the API
    :return: a trained or untrained model from the sklearn-classification package
    """

    if not isinstance(classification_config, dict):
        raise ex.InvalidConfigException("Wrong data structure of configuration: " + str(classification_config))

    try:
        new_classifier_method, datasource_classifier, event = get_config_parameter(classification_config)

        if new_classifier_method != "":
            exec_string = classification_config["classification_method_options"][new_classifier_method]
            return eval(exec_string)
    except KeyError:
        raise ex.InvalidConfigException("No Key found in configuration ")#evtl. genauere aufteilung der Exception notwendig

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        raise ex.InvalidConfigException("Wrong configuration values for loading")

    if event in classifier_dictionary.keys():
        model = classifier_dictionary[event]
    else:
        raise ex.InvalidConfigException("No such key for event: " + str(event))

    if model == "":
        return sklearn.svm.SVC()  # TODO: hardcoden oder noch entscheiden durch Analyse
    else:
        return model


def persist_classifier(classifier, classification_config):
    """
    name in documentation: 'klassifizierer_persistieren'

    This method takes a trained or newly created classifier an writes it into the according dictionary which is
    pickled subsequently.

    :param classifier:(sklearn-object) a classification algorithm form the sklearn package
    :param classification_config: configuration file with required parameters

    :raises InvalidConfigException: Raised if no access or wrong values inside of the configuration
    :raises PersistorException: Raised if classifier is not an instance of sklearn
    :return int: Statuscode, der angibt ob Perstistierung erfolgreich war(0 Erfolg, 1 Misserfolg)
    """

    if not isinstance(classification_config, dict):
        raise ex.InvalidConfigException("Wrong data structure of configuration: " + str(classification_config))

    try:
        new_classifier_method, datasource_classifier, event = get_config_parameter(classification_config)
    except KeyError:
        raise ex.InvalidConfigException("Wrong key for Configuration")

    if not (isinstance(classifier, sklearn.svm.SVC) | isinstance(classifier, sklearn.neighbors._classification.KNeighborsClassifier)):
        raise ex.PersistorException("Not a valid classification model")

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        raise ex.InvalidConfigException("Wrong configuration values for loading")

    if event in classifier_dictionary.keys():
        classifier_dictionary[event] = classifier
    else:
        raise ex.InvalidConfigException("No such key for event: " + str(event))

    save_dictionary(classifier_dictionary, datasource_classifier)
    return 0


def load_dictionary(datasource_classifier):
    """
    Loads the dictionary containing all the available classifcation-models for the events with pickle.

    :raises InvalidConfigException: Raised when there is nothing to unpickle e.g. the file is empty

    :param datasource_classifier: the file in which the dictionary is currently stored
    :return dictionary: unpickled dictionary {"event_name": sklearn-model}
    """

    with open(datasource_classifier, "rb") as file:
        try:
            content = pickle.load(file)
        except EOFError:
            raise ex.InvalidConfigException("No content in the specified file: " + str(datasource_classifier))

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
    new_classifier_method = config["new_classifier_method"]
    datasource_classifier = config["datasource_classifier"]
    event = config["selected_event"]
    return new_classifier_method, datasource_classifier, event
