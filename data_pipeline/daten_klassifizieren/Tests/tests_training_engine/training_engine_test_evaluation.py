import unittest
from mockito.matchers import ANY
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.daten_klassifizieren.training_engine as training_engine
from data_pipeline.daten_klassifizieren.training_engine import get_config_parameter
from data_pipeline.konfiguration.src.config import classification_config as config
from sklearn.model_selection import train_test_split
import numpy as np

from data_pipeline.daten_klassifizieren.training_engine import convert_time


class TestEvaluateClassifier(unittest.TestCase):

    def test_returns_true(self):
        """
        this method tries to test if the requires score in the config is greater than the new score
        :return: true
        """
        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5,
                               "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
            "timeframe": ["2020-01-14 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
            "datasource_marked_data": {'database': 'nilan_marked', 'measurement': 'training'},
            "classification_method_options": {
                "SVM": "sklearn.svm.SVC()",
                "kNN": "sklearn.neighbors.KNeighborsClassifier()"
            },
            "create_new_classifier": "True",
            "datasource_classifier": 'model_training_engine.txt'

        }

        selected_event, required_score, test_size, datasource_marked_data, start_time, end_time = get_config_parameter(
            classification_config)
        classifier = model_persistor.load_classifier(config)
        start_time = convert_time(start_time)
        end_time = convert_time(end_time)
        df = read_manager.read_query(datasource_marked_data,
                                     f"SELECT * FROM {selected_event} WHERE time >= {start_time}ms "
                                     f"AND time <= {end_time}ms")
        df.dropna(inplace=True)
        y = np.array(df[selected_event])
        X = np.array(df.drop(labels=[selected_event, f"{selected_event}_marker"], axis=1))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(test_size))

        self.assertEqual(training_engine.evaluate_classifier(classifier, required_score, X_test, y_test), True)

    def test_returns_false(self):
        """
        does the same like above but with a higher require score in the config
        :return:
        """

        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 1.0, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5,
                               "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
            "timeframe": ["2020-01-14 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
            "datasource_marked_data": {'database': 'nilan_marked', 'measurement': 'training'},
            "classification_method_options": {
                "SVM": "sklearn.svm.SVC()",
                "kNN": "sklearn.neighbors.KNeighborsClassifier()"
            },
            "create_new_classifier": "True",
            "datasource_classifier": 'model.txt'

        }

        selected_event, required_score, test_size, datasource_marked_data, start_time, end_time = get_config_parameter\
            (classification_config)
        classifier = model_persistor.load_classifier(config)
        start_time = convert_time(start_time)
        end_time = convert_time(end_time)
        df = read_manager.read_query(datasource_marked_data,
                                 f"SELECT * FROM {selected_event} WHERE time >= {start_time}ms "
                                 f"AND time <= {end_time}ms")
        df.dropna(inplace=True)
        y = np.array(df[selected_event])
        X = np.array(df.drop(labels=[selected_event, f"{selected_event}_marker"], axis=1))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(test_size))
        classifier = classifier.fit(X_train, y_train)

        self.assertEqual(training_engine.evaluate_classifier(classifier, required_score, X_test, y_test), False)



if __name__ == '__main__':
    unittest.main()
