import unittest
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor


class test_load_classifier(unittest.TestCase):

    '''
    #Blackbox-Testing
        Äquivalenzklassen
        Randwertanalyse
    #Whitebox-Testing
        Codecoverage
    '''

    ###Blackbox
    # 1. config not a JSON/dictionary
    # 2. config does not contain a value
    # - config does not contain a key
    # - code cannot evaluate string from "classification_method_options
    # - code cannot find "datasource_classifier"
    # - load dictionary exception
    # 4.
    def test_returns_existing_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "datasource_classifier": "data_pipeline/daten_klassifizieren/unittest/model_test_returns_existing_classifier.txt",
            "new_classifier_method": ""
        }
        self.assertTrue(model_persistor.load_classifier(classification_config))


    def test_returns_not_existing_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "datasource_classifier": "data_pipeline/daten_klassifizieren/unittest/model_test_returns_not_existing_classifier.txt",
            "new_classifier_method": ""
        }
        classifier_dictionary = model_persistor.load_dictionary("data_pipeline/daten_klassifizieren/unittest/model_test_returns_not_existing_classifier.txt")
        classifier_dictionary["abtauzyklus"] = ""
        model_persistor.save_dictionary(classifier_dictionary, "data_pipeline/daten_klassifizieren/unittest/model_test_returns_not_existing_classifier.txt")
        self.assertTrue(model_persistor.load_classifier(classification_config))


if __name__ == '__main__':
    unittest.main()

