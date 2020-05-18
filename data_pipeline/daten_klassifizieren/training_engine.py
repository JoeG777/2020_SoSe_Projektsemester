import data_pipeline.exception.exceptions as exce
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime
import time
from data_pipeline.daten_klassifizieren.classification_API import logger

def train_classifier(config):
    """Name in documentation: klassifizierer_trainieren()
    Train a classifier to identify a specific event.
    :param
        config: Contains parameters for training the classifier
    :raises
        InvalidConfigException
        PersistorException
    :return
        int: Status code that indicates whether the training was successful(0 Success, 1 Failure)"""
    try:
        logger.info("Logging config")
        selected_event, required_score, test_size, datasource_marked_data, start_time, end_time = get_config_parameter(config)
    except Exception:
        return exce.InvalidConfigValueException
    try:
        logger.info("Logging Model")
        classifier = model_persistor.load_classifier(config)
    except Exception as e:
        raise exce.PersistorException(str(e)) # TODO: warum nochmal eine werfen, wenn eh schon geworfen???
    start_time = convert_time(start_time)
    end_time = convert_time(end_time)
    df = read_manager.read_query(datasource_marked_data, f"SELECT * FROM {selected_event} WHERE time >= {start_time}ms "
                                                      f"AND time <= {end_time}ms")
    df.dropna(inplace=True)
    y = np.array(df[selected_event])
    X = np.array(df.drop(labels=[selected_event, f"{selected_event}_marker"], axis=1))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    try:
        logger.info("training Model")
        classifier = classifier.fit(X_train, y_train)
    except Exception:
        return 1

    if evaluate_classifier(classifier, required_score, X_test, y_test):
        model_persistor.persist_classifier(classifier, config)
        logger.info("Saving Model")
    return 0


def evaluate_classifier(classifier, required_score, X_test, y_test):
    """Name in documentation: klassifizierer_bewerten()
    After the classifier has already been optimized based on the training data, a scoring based on test data takes place
    :param
        classifier: Classifier intended for evaluation
        required_score: Already existing score
        X_test: Test data for evaluation
        y_test: Test data for evaluation
    :raises
    :return
        boolean: True: New Classifier has a higher score and will be persist, False: New Classifier has a lower score and will not be persist)"""
    # TODO : ursprünglicher und neuer Score loggen
    score = classifier.score(X_test, y_test)
    print("Das ist der alte Score: ", required_score)
    print("Das ist der neue Score: ", score)
    if score >= required_score:
        logger.info("evaluating Model")
        return True
    return False


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param
        config: dictionary from which the parameters will be extracted
    :raises
    :return
        string: selected_event: selected classification event
        float: required_score: required score for the classifier
        string: test_size: proportion of test and training data size
        string: datasource_marked_data: database name for the marked_data
        array: timeframe: timeframe for the query of the required data
        """
    selected_event = config['selected_event']
    required_score = config['required_score'][selected_event]
    test_size = config['test_size']
    timeframe = config['timeframe']
    datasource_marked_data = config['datasource_marked_data']['database']
    return selected_event, required_score, test_size, datasource_marked_data, timeframe[0], timeframe[1]


def convert_time(time_var):
    """Convert a given date and time to unix timestamp
    :param
        time_var: date and time to convert
    :raises
    :return
        int: The converted time as unix timestamp"""
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000

if __name__ == "__main__":
    train_classifier(config)