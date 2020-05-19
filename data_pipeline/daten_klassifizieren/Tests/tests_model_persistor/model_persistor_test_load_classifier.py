import unittest
import pickle
import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex
from sklearn.neighbors import KNeighborsClassifier
import sklearn
import copy


class test_load_classifier(unittest.TestCase):
    model = KNeighborsClassifier()

    def setUp(self):
        self.config = copy.deepcopy(config)
        self.config['create_new_classifier'] = ""

    def test_returns_existing_classifier(self):
        classification_config = copy.deepcopy(self.config)
        classification_config['datasource_classifier'] = "test_models/model_test_returns_existing_classifier.txt"
        self.assertTrue(isinstance(mp.load_classifier(classification_config), type(self.model)))

    def test_returns_not_existing_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "datasource_classifier": "test_models/model_test_returns_existing_classifier.txt",
            "create_new_classifier": ""
        }
        classifier_dictionary = mp.load_dictionary("test_models/model_test_returns_existing_classifier.txt")
        classifier_dictionary["abtauzyklus"] = ""
        mp.save_dictionary(classifier_dictionary, "test_models/model_test_returns_existing_classifier.txt")
        self.assertTrue(mp.load_classifier(classification_config))

    def test_wrong_structure_config(self):
        string = "Hallo"
        with self.assertRaises(ex.ConfigTypeException):
            mp.load_classifier(string)



    def test_datasource_classifier_none(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config["datasource_classifier"] = None

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config)

    def test_datasource_classifier_empty(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = ""

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config)

    def test_datasource_classifier_is_wrong(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = "i_am_not_an_existing_file.yeah"

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config)

    def test_datasource_classifier_unpicklable(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = "test_models/unpicklable_model.txt"

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config)

    def test_datasource_classifier_IOerror(self):
        pass

    def test_classifier_dictionary_for_event_is_none(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = 'test_models/model_returns_code_0.txt'
        wrong_config['create_new_classifier'] = ""
        wrong_config['selected_event'] = None

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.load_classifier(wrong_config)

    def test_classifier_dictionary_for_event_is_empty(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        wrong_config['selected_event'] = ""

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.load_classifier(wrong_config)

    def test_classifier_dictionary_for_event_is_wrong(self):
        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        wrong_config['selected_event'] = "Was ist denn mit Carsten los?"

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.load_classifier(wrong_config)

    def test_model_at_event_is_empty_returns_SVC(self):
        test_config = copy.deepcopy(self.config)
        test_config['datasource_classifier'] = "test_models/model_test_returns_not_existing_classifier.txt"

        self.assertTrue(isinstance(mp.load_classifier(test_config), type(self.model)))

    def test_model_for_event_is_not_instance_of_sklearn(self):
        path_to_wrong_dictionary = "test_models/model_returns_code_0_contains_wrong_model_at_abauzyklus.txt"
        classifier_dictionary = mp.load_dictionary(path_to_wrong_dictionary)
        classifier_dictionary['abtauzyklus'] = "Ich bin kein richtiges Model"
        mp.save_dictionary(classifier_dictionary, path_to_wrong_dictionary)

        wrong_config = copy.deepcopy(self.config)
        wrong_config['datasource_classifier'] = path_to_wrong_dictionary

        test_model = mp.load_classifier(wrong_config)
        self.assertTrue(isinstance(test_model, type(self.model)))

    def test_new_classifer_method_is_not_empty(self):
        test_config = copy.deepcopy(self.config)
        test_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        test_config['create_new_classifier'] = "True"
        test_model = mp.load_classifier(test_config)

        self.assertTrue(isinstance(test_model, sklearn.neighbors.KNeighborsClassifier().__class__))

    def test_for_existing_models_in_dictionary(self):
        test_config = copy.deepcopy(self.config)
        test_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        test_config['selected_event'] = "warmwasseraufbereitung"
        mp.persist_classifier(self.model, test_config)

        existing_model = mp.load_classifier(test_config)
        self.assertTrue(isinstance(existing_model, (sklearn.neighbors.KNeighborsClassifier, sklearn.svm.SVC)))


if __name__ == '__main__':
    unittest.main()
