import unittest
import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex
from sklearn.svm import SVC
from sklearn import neighbors


class test_load_classifier(unittest.TestCase):
    model = SVC()

    def test_returns_existing_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "datasource_classifier": "test_models/model_test_returns_existing_classifier.txt",
            "new_classifier_method": ""
        }
        self.assertTrue(mp.load_classifier(classification_config))

    def test_returns_not_existing_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "datasource_classifier": "test_models/model_test_returns_existing_classifier.txt",
            "new_classifier_method": ""
        }
        classifier_dictionary = mp.load_dictionary("test_models/model_test_returns_existing_classifier.txt")
        classifier_dictionary["abtauzyklus"] = ""
        mp.save_dictionary(classifier_dictionary, "test_models/model_test_returns_existing_classifier.txt")
        self.assertTrue(mp.load_classifier(classification_config))

    def test_wrong_structure_config(self):
        str = "Hallo"
        with self.assertRaises(ex.InvalidConfigException):
            mp.load_classifier(str)

    def test_param_new_classifier_none(self):
        wrong_config = config.copy()
        wrong_config["new_classifier_method"] = None

        with self.assertRaises(ex.InvalidConfigException):
            mp.load_classifier(wrong_config)

    def test_classifier_dictionary_for_event_is_none(self):
        wrong_config = config.copy()
        wrong_config['new_classifier_method'] = ""
        wrong_config['selected_event'] = None

        with self.assertRaises(ex.InvalidConfigException):
            mp.load_classifier(wrong_config)


if __name__ == '__main__':
    unittest.main()

