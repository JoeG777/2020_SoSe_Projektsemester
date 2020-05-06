import unittest
from mockito import mockito
from data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine import training_engine as tm


class test_model_to_dict(unittest.TestCase):
    def test_all_values_contained(self):
        test_score = 1.0
        test_model = "model"
        test_dependent_data_keys = "keys"
        test_dict = {
            "dependent": test_dependent_data_keys,
            "score": float(test_score),
            "model": test_model
        }

        output = tm.model_to_dict(test_score, test_model, test_dependent_data_keys)

        self.assertDictEqual(output, test_dict)


class test_train_model(unittest.TestCase):
    def test_all_values_contained(self):
        mockito.when()
        test_data = ""
        test_prediction_unit = ""



if __name__ == '__main__':
    unittest.main()