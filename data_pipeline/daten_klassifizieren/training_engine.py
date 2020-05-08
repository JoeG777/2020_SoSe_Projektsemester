import sklearn
import pandas as pd
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.log_writer as log_writer
from data_pipeline.daten_klassifizieren.config import classification_config as config
from sklearn.model_selection import train_test_split
import numpy as np


def train_classifier(config):
    selected_event, required_score, test_size, datasource_training_data = get_config_parameter(config)
    classifier = model_persistor.load_classifier(config)
    df = read_manager.read_data(datasource_training_data, measurement='training', register=None, resolve_register=None,
                                start_utc=None, end_utc=None)
    df.dropna(inplace=True)
    y = np.array(df['Abtauzyklus'])#selected_event
    X = np.array(df.drop(labels=['Abtauzyklus', 'Abtaumarker'], axis=1))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    classifier = classifier.fit(X_train, y_train)
    if evaluate_classifier(classifier, required_score, X_test, y_test):
        model_persistor.persist_classifier(classifier, config)
    return 0


def evaluate_classifier(classifier, required_score, X_test, y_test):
    score = classifier.score(X_test, y_test)
    if score >= required_score:
        return True
    return False


def get_config_parameter(config):
    selected_event = config['selected_event']
    required_score = config['required_score'][selected_event]
    test_size = config['test_size']
    datasource_training_data = config['datasource_training_data']['database']
    return selected_event, required_score, test_size, datasource_training_data