import unittest
import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex
from sklearn.svm import SVC


class test_persist_classifier (unittest.TestCase):
    config_test = config
    model_dictionary = {"abtauzyklus":"",
                        "warmwasseraufbereitung":"",
                        "ofennutzung":"",
                        "luefterstufen":""}
    model = SVC()

    def test_returns_statuscode_0(self):
        self.beforeTest(self.model_dictionary)

        self.assertEqual(mp.persist_classifier(self.model,  self.config_test), 0)


    def test_wrong_structure_congfig(self):
        str = "Hallo"
        with self.assertRaises(ex.ConfigTypeException):
            mp.persist_classifier(self.model, str)


    def test_param_not_a_sklearn_model(self):
        self.beforeTest(self.model_dictionary)
        model_wrong = "Hallo"

        with self.assertRaises(ex.PersistorException):
            mp.persist_classifier(model_wrong, self.config_test)


    def test_no_model_dictionary_in_datasource_classifier(self):
        wrong_config = self.config_test.copy()
        wrong_config['datasource_classifier'] = 'test_models/model_empty.txt'
        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model, wrong_config)


    def test_param_datasource_classifier_wrong(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        wrong_config['datasource_classifier'] = "Hallo" # <- not valid source

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model,  wrong_config)


    def test_param_datasource_classifier_empty(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        wrong_config['datasource_classifier'] = "" # <- not valid source

        with self.assertRaises(ex.InvalidConfigValueException):
            mp.persist_classifier(self.model,  wrong_config)


    def test_param_datasource_classifier_key_not_there(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        del wrong_config['datasource_classifier']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model, wrong_config)


    def test_param_event_no_key(self):
        self.beforeTest(self.model_dictionary)
        wrong_key_config = self.config_test.copy()
        del wrong_key_config['selected_event']

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model,  wrong_key_config)


    def test_param_event_none_value(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        wrong_config['selected_event'] = None

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model,  wrong_config)


    def test_param_event_empty_string_value(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        wrong_config['selected_event'] = ""
        print("Hier", wrong_config['selected_event'])

        with self.assertRaises(ex.InvalidConfigKeyException):
            mp.persist_classifier(self.model,  wrong_config)


    def test_param_event_no_valid_value(self):
        self.beforeTest(self.model_dictionary)
        wrong_config = self.config_test.copy()
        wrong_config['selected_event'] = "Hallo"

        with self.assertRaises(ex.InvalidConfigKeyException):
                mp.persist_classifier(self.model, wrong_config)



    '''
    Sets the parameter of the pickled-file to a test file and saves a test dictionary in it
    '''
    def beforeTest(self, pickled_dictionary):
        self.config_test['datasource_classifier'] = 'model_returns_code_0.txt'
        mp.save_dictionary(pickled_dictionary, 'model_returns_code_0.txt')


if __name__ == '__main__':
    unittest.main()
