import unittest
import requests
from mockito import *
from mockito.matchers import ANY

import data_pipeline.exception.exceptions as ex
from data_pipeline.daten_klassifizieren import classification_engine as classification
from data_pipeline.daten_klassifizieren.config import classification_config as config


class test_classify(unittest.TestCase):

    url = 'http://127.0.0.1:5000/classify'

    def test_response_200(self):
        request = requests.post(self.url, json=config)
        when2(classification.apply_classifier, config).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)

    def test_for_900(self):
        wrong_config = config.copy()
        del wrong_config['new_classifier_method']
        request = requests.post(self.url, json=wrong_config)

        when2(classification.apply_classifier, wrong_config).thenRaise(ex.ConfigTypeException)
        response = request.status_code
        self.assertEqual(response, 900)

    '''def test_invalid_config(self):
        request = requests.post(self.url, json="Hallo")
        when2(classification.apply_classifier, config).thenReturn(ex.ConfigTypeException)
        response = request.status_code
        self.assertEqual(response, 900)
    '''

    def test_for_901(self):
        request = requests.post(self.url, json=config)

        when2(classification.apply_classifier, config).thenThrow(ex.DBException)
        response = request.status_code
        self.assertEqual(response, 901)

    def test_for_902(self):
        request = requests.post(self.url, json=config)

        when2(classification.apply_classifier, ANY).thenRaise(ex.PersistorException)
        response = request.status_code
        self.assertEqual(response, 902)

    def test_for_903(self):
        pass

    @classmethod
    def setUp(cls):
        unstub()
        spy2(classification.apply_classifier)


if __name__ == '__main__':
    unittest.main()
