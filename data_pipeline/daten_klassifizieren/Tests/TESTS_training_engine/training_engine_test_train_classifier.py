import unittest
import data_pipeline.daten_klassifizieren.training_engine as training_engine
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
from data_pipeline.daten_klassifizieren.config import classification_config


class test_train_classifier(unittest.TestCase):

    def test_get_config(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5, "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
        }




    def test_get_classifier(self):
        classification_config = {
            "selected_event": "abtauzyklus",
            "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.2, "offennutzung": 0.5, "luefterstufen": 0.8},
            "test_size": 0.3,
            "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
        }
        existing_classifier = model_persistor.load_classifier(classification_config)
        #training_engine.train_classifier(classification_config)
        self.assertEqual(existing_classifier,)

if __name__ == '__main__':
    unittest.main()
