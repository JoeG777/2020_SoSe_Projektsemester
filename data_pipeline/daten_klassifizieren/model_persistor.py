import sklearn
from sklearn import neighbors
from sklearn import svm
import pickle
import data_pipeline.exception.exceptions as ex


def load_classifier(classification_config, current_model_type, called_from_training_engine=False):
    """
    Name in documentation: 'klassifizierer_laden'

    This method loads either an existing model for a specific event or creates an entirely new one from a specified
    algorithm

    :param current_model_type: Holds the event for which the model should be loaded
    :param classification_config: provided by the API
    :param called_from_training_engine: specifies where the method was called
    :raises ConfigTypeException: Raised if configuration not of type 'dict'
    :raises InvalidConfigKeyException: Raised if a key in the config does not exist
    :raises InvalidConfigValueException: Raised if a value inside of the config is wrong

    :return: a trained or untrained model from the sklearn-classification package
    """

    if not isinstance(classification_config, dict):
        raise ex.ConfigTypeException("Wrong data structure of configuration: " + str(classification_config))

    try:
        create_new_classifier, datasource_classifier, event = get_config_parameter(classification_config)
        if (create_new_classifier == "True") and called_from_training_engine:
            return neighbors.KNeighborsClassifier()
    except KeyError:
        raise ex.InvalidConfigKeyException("No Key found in configuration ")

    try:
        classifier_dictionary = load_dictionary(datasource_classifier)
    except Exception:
        raise ex.InvalidConfigValueException("Wrong configuration values for loading")

    if current_model_type in classifier_dictionary.keys():
        model = classifier_dictionary[current_model_type]
    else:
        raise ex.InvalidConfigKeyException("No such key for event: " + str(current_model_type))

    if model == '':
        return neighbors.KNeighborsClassifier()
    else:
        return model


def persist_classifier(classifier, classification_config, current_model_type):
    """
    name in documentation: 'klassifizierer_persistieren'

    This method takes a trained or newly created classifier an writes it into the according dictionary which is
    pickled subsequently.

    :param current_model_type:  Holds the event for which the model should be loaded
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

    if not (isinstance(classifier, svm.SVC) | isinstance(classifier, neighbors.KNeighborsClassifier)):
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
    name in documentation: 'dictionary_laden'

    Loads the dictionary containing all the available classifcation-models for the events with pickle.

    :param datasource_classifier: the file in which the dictionary is currently stored

    :raises InvalidConfigValueException: Raised when there is nothing to unpickle e.g. the file is empty

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
    name in documentation: 'dictionary_speichern'
     Saves the dictionary containing all the available classifcation-models for the events with pickle.

    :param classifier_dictionary: dictionary {"event_name": sklearn-model}
    :param datasource_classifier: the file in which the dictionary should be stored

    :return: void
    """

    with open(datasource_classifier, "wb") as file:
        pickle.dump(classifier_dictionary, file)


def get_config_parameter(config):
    """
    name in documentation: 'konfig_parameter_abrufen'

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
