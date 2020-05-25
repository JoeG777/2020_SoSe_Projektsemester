import sklearn
import pandas as pd
import data_pipeline.exception.exceptions as exce
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
from sklearn.model_selection import train_test_split
from data_pipeline.daten_klassifizieren.training_data_time_points import event_start_end_timestamp as markers
import numpy as np
from datetime import datetime
import time
from data_pipeline.daten_klassifizieren.classification_API import logger


def train_classifier(config):

    """
    Name in documentation: klassifizierer_trainieren()

    Train a classifier to identify a specific event.
    :param classification_config: Contains parameters for training the classifier
    :param classifier:(sklearn-object) a classification algorithm form the sklearn package
    :raises InvalidConfigValueException:Raised if a value inside of the config is wrong
    :raises  PersistorException: Raised if classifier is not an instance of sklearn
    :return int: Status code that indicates whether the training was successful(0 Success, 1 Failure)"""
    try:
        selected_event, required_score, test_size, datasource_marked_data, start_time, end_time, events = get_config_parameter(config)
    except Exception:
        raise exce.InvalidConfigValueException
    logger.info("config parameter loaded")
    try:
        start = convert_time(start_time)
        end = convert_time(end_time)
    except Exception as e:
        raise exce.InvalidConfigValueException(str(e))
    df = read_manager.read_query(datasource_marked_data, f"SELECT * FROM {selected_event} WHERE time >= {start}ms AND time <= {end}ms")
    for event in events:
        end_start = markers[event]
        start_event = list(end_start.keys())[0]
        end_event = list(end_start.values())[len(end_start)-1]
        if (str(df.index[0]) > start_event) or (str(df.index[-1]) < end_event):
            raise exce.ConfigException('time frame of trainingsdata not in selected data frame included')
        df_copy = df.copy()[start_event:end_event]

        try:
            classifier = model_persistor.load_classifier(config, event, True)
        except Exception as e:
            raise exce.PersistorException(str(e))
        logger.info("model loaded")
        df_copy.dropna(inplace=True)
        y = np.array(df_copy[event])
        for drop_event in events:
            df_copy = df_copy.drop(labels=[drop_event, f"{drop_event}_marker"], axis=1)
        X = df_copy.to_numpy()
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        except Exception as e:
            raise exce.SklearnException(str(e))
        try:
            classifier = classifier.fit(X_train, y_train)
        except Exception as e:
            raise exce.SklearnException(str(e))
        logger.info("model trained")
        if evaluate_classifier(classifier, required_score[event], X_test, y_test):
            model_persistor.persist_classifier(classifier, config, event)
            logger.info('model persisted')
        else:
            logger.info('score too low, model not persisted')
    return 0


def evaluate_classifier(classifier, required_score, X_test, y_test):
    """Name in documentation: klassifizierer_bewerten()
    After the classifier has already been optimized based on the training data, a scoring based on test data takes place

    :param classifier: Classifier intended for evaluation
    :param required_score: Already existing score
    :param X_test: Test data for evaluation
    :param y_test: Test data for evaluation
    :return boolean: True: New Classifier has a higher score and will be persist, False: New Classifier has a lower score and will not be persist)"""
    score = classifier.score(X_test, y_test)
    logger.info("new score: " + str(score))
    if score >= required_score:
        return True
    return False


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param classification_config: dictionary from which the parameters will be extracted
    :return string: selected_event: selected classification event
    :return   float: required_score: required score for the classifier
    :return  string: test_size: proportion of test and training data size
    :return string: datasource_marked_data: database name for the marked_data
    :return array: timeframe: timeframe for the query of the required data
            """
    selected_event = config['selected_event']
    events = config[selected_event]
    required_score = config['required_score']
    test_size = config['test_size']
    timeframe = config['timeframe']
    datasource_marked_data = config['datasource_marked_data']['database']
    return selected_event, required_score, test_size, datasource_marked_data, timeframe[0], timeframe[1], events


def convert_time(time_var):
    """Convert a given date and time to unix timestamp
    :param time_var: date and time to convert
    :return int: The converted time as unix timestamp"""
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple()))) * 1000


if __name__ == "__main__":
    train_classifier()
