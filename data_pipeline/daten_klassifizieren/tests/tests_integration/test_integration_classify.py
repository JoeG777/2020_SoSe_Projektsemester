import copy
import unittest
import requests

from data_pipeline.daten_klassifizieren.config import classification_config as config


class test_classify(unittest.TestCase):
    url = 'http://127.0.0.1:5000/classify'

    def test_response_200_with_abtauzyklus(self):

        request = requests.post(self.url, json=config)
        response = request.status_code

        self.assertEqual(response, 200)

    def test_invalid_config(self):

        request = requests.post(self.url, json="Hallo")
        response = request.status_code

        self.assertEqual(response, 900)

    def test_for_900(self):
        wrong_config = ""
        request = requests.post(self.url, json=wrong_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_for_901(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['datasource_raw_data']['database'] = 'notanactualdatabase'
        request = requests.post(self.url, json=wrong_config)
        response = request.status_code

        self.assertEqual(response, 901)

    def test_for_903(self):
        pass

    def test_datasource_raw_data_missing(self):
        test_config = copy.deepcopy(config)
        del test_config['datasource_raw_data']

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_raw_data_None(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = None

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_raw_data_wrong_type(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = "Hallo, ich bin keine Datenbank"

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_raw_data_database_not_existing(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = {'database': 'ich_existiere_nicht', 'measurement': 'temperature'}

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 901)

    def test_datasource_raw_data_measurement_missing(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = {'database': 'test'}

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_classifier_missing(self):
        test_config = copy.deepcopy(config)
        del test_config['datasource_classifier']

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_classifier_none(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = None

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_classifier_empty(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = ""

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_classifier_wrong_file(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = "model_empty_API.txt"

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)

    def test_datasource_classifier_unpicklable(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classifier'] = "model_unpicklable_API.txt"

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        self.assertEqual(response, 900)


if __name__ == '__main__':
    unittest.main()
