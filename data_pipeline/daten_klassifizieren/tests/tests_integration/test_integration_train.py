import unittest
import requests
import copy

import data_pipeline.exception.exceptions as ex
import data_pipeline.daten_klassifizieren.classification_engine as classification
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as editing
import data_pipeline.daten_klassifizieren.training_engine as training

from data_pipeline.daten_klassifizieren.config import classification_config as config


class test_train(unittest.TestCase):
    url = 'http://127.0.0.1:5000/train'

    def test_response_200(self):
        request = requests.post(self.url, json=config)
        response = request.status_code

        self.assertEqual(response, 200)

    def test_invalid_config(self):
        request = requests.post(self.url, json=123)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_enrich_for_key_exception(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['selected_event']
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 900)

    def test_enrich_for_invalid_value_exception(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['timeframe'] = ["2020-01-12 00:00:00.000 UTC", "ich_bin_kein_datum"]
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 900)

    def test_enrich_for_db_exception(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_raw_data'] = {'database': 'test_measurement', 'measurement': 'kein_measurement'}
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 901)

# mark
    def test_mark_for_invalid_key_exception(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['timeframe']
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 900)

    def test_mark_for_invalid_value_exception(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['timeframe'] = ["2020-01-12 00:00:00.000 UTC", "ich_bin_kein_datum"]
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 900)

    def test_mark_for_db_exception(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_enriched_data'] = {'database': 'nicht_enriched', 'measurement': 'training'}
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 901)

# train
    def test_train_for_invalid_config_value(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['datasource_marked_data']
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 900)

    def test_train_for_persistor_exception(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_classifier'] = 'model_empty_API.txt'
        request = requests.post(self.url, json=wrong_config)

        response = request.status_code
        self.assertEqual(response, 902)

    '''def test_train_for_exception_predict_returns_1(self):
        test_query = "SELECT * FROM abtauzyklus WHERE time >= 1578783600000ms AND time <= 1579474800000ms"
        wrong_config = copy.deepcopy(config)
        wrong_config['selected_event'] = 'abtauzyklus'
        request = requests.post(self.url, json=wrong_config)
        response = request.status_code

        self.assertEqual(response, 901)
    '''

    def test_for_901(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_raw_data']['database'] = "notanactualdatabase"
        wrong_config['selected_event'] = "standard"
        request = requests.post(self.url, json=wrong_config)
        response = request.status_code

        self.assertEqual(response, 901)

    def test_for_902(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = 'model_empty.txt'

        request = requests.post(self.url, json=test_config)

        response = request.status_code
        self.assertEqual(response, 902)

    def test_for_903(self):
        pass


if __name__ == '__main__':
    unittest.main()
