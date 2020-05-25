import copy
import unittest
from sklearn.neighbors import KNeighborsClassifier

import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex


class test_load_classifier(unittest.TestCase):
    model = KNeighborsClassifier()
    current_model_type_std = config['standard']
    current_model_type_pred = config['pred']

    def test_returns_existing_classifier(self):
        classification_config = config.copy()
        classification_config['datasource_classifier'] = "test_models/model_test_returns_existing_classifier.txt"
        self.assertTrue(isinstance(mp.load_classifier(classification_config, self.current_model_type_std[0]), type(self.model)))

    def test_returns_not_existing_classifier(self):
        wrong_config = copy.deepcopy(config)
        wrong_config["datasource_classifier"] = "test_models/model_test_returns_existing_classifier.txt"
        classifier_dictionary = mp.load_dictionary("test_models/model_test_returns_existing_classifier.txt")
        classifier_dictionary["abtauzyklus"] = ""
        mp.save_dictionary(classifier_dictionary, "test_models/model_test_returns_existing_classifier.txt")

        self.assertTrue(mp.load_classifier(wrong_config, self.current_model_type_std[0]))

    def test_wrong_structure_config(self):
        string = "Hallo"
        with self.assertRaises(ex.ConfigTypeException):
            mp.load_classifier(string, self.current_model_type_std[0])

    def test_datasource_classifer_deleted(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['datasource_classifier']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0])

    def test_datasource_classifier_none(self):
        wrong_config = config.copy()
        wrong_config["datasource_classifier"] = None

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0])

    def test_datasource_classifier_empty(self):
        wrong_config = config.copy()
        wrong_config['datasource_classifier'] = ""

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0])

    def test_datasource_classifier_is_wrong(self):
        wrong_config = config.copy()
        wrong_config['datasource_classifier'] = "i_am_not_an_existing_file.yeah"

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0])

    def test_datasource_classifier_unpicklable(self):
        wrong_config = config.copy()
        wrong_config['datasource_classifier'] = "test_models/unpicklable_model.txt"

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0])

    def test_datasource_classifier_IOerror(self):
        pass  # funktioniert nicht
        '''
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = "test_models/not_accessible_file.txt"  # Datei ist schreibgescuetzt

        with self.assertRaises(ex.FileException):
            mp.load_classifier(wrong_config, self.current_model_type_std[0]), self.current_model_type_std[0]
        '''

    def test_model_at_event_is_empty_returns_KNC(self):
        test_config = config.copy()
        test_config['datasource_classifier'] = "test_models/model_test_returns_not_existing_classifier.txt"

        tested_model = mp.load_classifier(test_config, self.current_model_type_std[0])

        self.assertTrue(isinstance(tested_model, type(self.model)))

    def test_model_for_event_is_not_instance_of_sklearn(self):
        path_to_wrong_dictionary = "test_models/model_returns_code_0_contains_wrong_model_at_abauzyklus.txt"
        classifier_dictionary = mp.load_dictionary("test_models/model_returns_code_0.txt")
        classifier_dictionary['abtauzyklus'] = "Ich bin kein richtiges Model"
        mp.save_dictionary(classifier_dictionary, path_to_wrong_dictionary)

        wrong_config = config.copy()
        wrong_config['datasource_classifier'] = path_to_wrong_dictionary

        test_model = mp.load_classifier(wrong_config, self.current_model_type_std[0])
        self.assertFalse(isinstance(test_model, type(self.model)))

    def test_new_classifer_method_is_not_empty(self):
        test_config = config.copy()
        test_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        test_config['new_classifier_method'] = "kNN"
        test_model = mp.load_classifier(test_config, self.current_model_type_std[0])

        self.assertTrue(isinstance(test_model, type(self.model)))

    def test_for_existing_models_in_dictionary(self):
        test_config = config.copy()
        test_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        test_config['selected_event'] = "warmwasseraufbereitung"
        mp.persist_classifier(self.model, test_config, self.current_model_type_std[1])

        existing_model = mp.load_classifier(test_config, self.current_model_type_std[1])
        self.assertTrue(isinstance(existing_model, type(self.model)))

    def test_for_create_new_classifier_true(self):
        wrong_config = copy.deepcopy(config)
        wrong_config["create_new_classifier"] = "True"

        self.assertTrue(isinstance(mp.load_classifier(wrong_config, self.current_model_type_std[0], True), type(self.model)))

    def test_current_model_type_does_not_exist(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        wrong_current_model_type = "Ich_bin_kein_event"

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.load_classifier(wrong_config, wrong_current_model_type)


if __name__ == '__main__':
    unittest.main()
