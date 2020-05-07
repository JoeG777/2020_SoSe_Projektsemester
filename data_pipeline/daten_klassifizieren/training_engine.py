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
    classifier = model_persistor.load_classifier(config)
    df = read_manager.read_data('nilan_erweitert', measurement='training', register=None, resolve_register=None,
                                start_utc=None, end_utc=None)
    df.dropna(inplace=True)
    y = np.array(df['Abtauzyklus'])
    X = np.array(df.drop(labels=['Abtauzyklus', 'Abtaumarker'], axis=1))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    classifier = classifier.fit(X_train, y_train)
    evaluate_classifier(classifier, config, X_test, y_test)
    return


def evaluate_classifier(classifier, config, X_test, y_test):
    score = classifier.score(X_test, y_test)
    print(score)
    return


def persist_classifier():
    return

train_classifier(config)