import unittest
import data_pipeline.daten_klassifizieren.training_engine as training_engine

import data_pipeline.exception.exceptions as ex


class TestTrainClassifier(unittest.TestCase):

    def test_returns_statuscode_0(self):

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
            "new_classifier_method": "kNN",
            "datasource_classifier": 'model.txt'

        }
        self.assertEqual(training_engine.train_classifier(classification_config), 0)



    def test_returns_InvalidConfig(self):
        '''this method tests the exception without some data

        :return:InvalidConfigException
        '''
        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5,
                               "luefterstufen": 0.8},
            "test_size": 0.3
        }
        self.assertEqual(training_engine.train_classifier(classification_config), ex.InvalidConfigValueException)

    def test_returns_noPersist(self):
        '''
        Tests with no new classifier method
        :return: PersistException
        '''
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
            "new_classifier_method": ""
        }
        self.assertEqual(training_engine.train_classifier(classification_config), ex.PersistorException)

    def test_returns_status_1(self):
        '''
        test the case with no model
        :return: 1
        '''
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
            "new_classifier_method": "KNN",
            "datasource_classifier": ''
        }
        self.assertEqual(training_engine.train_classifier(classification_config), 1)



if __name__ == '__main__':
    unittest.main()
