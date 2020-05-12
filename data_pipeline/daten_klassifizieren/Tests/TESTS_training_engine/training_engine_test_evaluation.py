import unittest
import data_pipeline.daten_klassifizieren.training_engine as training_engine
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor

class test_evaluation(unittest.TestCase):

    def test_lower_score(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5, "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
        }
        existing_classifier = model_persistor.load_classifier(classification_config)
        training_engine.train_classifier(classification_config)
        updated_classifier = model_persistor.load_classifier(classification_config)
        self.assertEqual(existing_classifier, updated_classifier)

    def test_higher_score(self):
        classification_config = {
            "selected_event": "warmwasseraufbereitung",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5, "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
        }
        existing_classifier = model_persistor.load_classifier(classification_config)
        training_engine.train_classifier(classification_config)
        updated_classifier = model_persistor.load_classifier(classification_config)
        self.assertNotEqual(existing_classifier, updated_classifier)

if __name__ == '__main__':
    unittest.main()
