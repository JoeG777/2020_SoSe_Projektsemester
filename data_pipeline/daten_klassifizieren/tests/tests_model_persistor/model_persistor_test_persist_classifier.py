import copy
import unittest
from sklearn.neighbors import KNeighborsClassifier

import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex


class test_persist_classifier (unittest.TestCase):
    model = KNeighborsClassifier()
    current_model_type_std = config['standard']
    current_model_type_pred = config['pred']
    model_dictionary = {"abtauzyklus":"",
                        "warmwasseraufbereitung":"",
                        "ofennutzung":"",
                        "luefterstufen":""}

    def test_returns_statuscode_0(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = 'test_models/model_returns_code_0.txt'

        self.assertEqual(mp.persist_classifier(self.model,  wrong_config, self.current_model_type_std[0]), 0)

    def test_wrong_structure_congfig(self):
        str = "Hallo"
        with self.assertRaises(ex.ConfigTypeException):
            mp.persist_classifier(self.model, str, self.current_model_type_std[0])

    def test_param_not_a_sklearn_model(self):
        self.beforeTest(self.model_dictionary)
        model_wrong = "Hallo"

        with self.assertRaises(ex.PersistorException):
            mp.persist_classifier(model_wrong, config, self.current_model_type_std[0])

    def test_no_model_dictionary_in_datasource_classifier(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = 'test_models/model_empty.txt'
        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model, wrong_config, self.current_model_type_std[0])

    def test_param_datasource_classifier_wrong(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = "Hallo" # <- not valid source

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model,  wrong_config, self.current_model_type_std[0])

    def test_param_datasource_classifier_empty(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = "" # <- not valid source

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model,  wrong_config, self.current_model_type_std[0])

    def test_param_datasource_classifier_key_not_there(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = copy.deepcopy(config)
        del wrong_config['datasource_classifier']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model, wrong_config, self.current_model_type_std[0])

    def test_param_event_no_key(self):
        self.beforeTest(self.model_dictionary)
        wrong_key_config = copy.deepcopy(config)
        del wrong_key_config['selected_event']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model,  wrong_key_config, self.current_model_type_std[0])

    def test_param_event_none_value(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = 'test_models/model_returns_code_0.txt'
        del wrong_config['selected_event']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model,  wrong_config, self.current_model_type_std[0])
            
    def test_for_UnpicklingError(self):
        test_config = config.copy()
        test_config['datasource_classifier'] = "test_models/unpicklable_model.txt"
        
        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model, test_config, self.current_model_type_std[0])

    def test_current_model_type_does_not_exist(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = "test_models/model_returns_code_0.txt"
        wrong_current_model_type = "Hallo"
        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model, test_config, wrong_current_model_type)


    '''
    Sets the parameter of the pickled-file to a test file and saves a test dictionary in it
    '''
    def beforeTest(self, pickled_dictionary):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = 'model_returns_code_0.txt'
        mp.save_dictionary(pickled_dictionary, 'model_returns_code_0.txt')


if __name__ == '__main__':
    unittest.main()
