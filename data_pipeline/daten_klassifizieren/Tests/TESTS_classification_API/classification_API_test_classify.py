import unittest
from mockito import *
import requests
import json
from data_pipeline.daten_klassifizieren.config import classification_config as config
from data_pipeline.daten_klassifizieren import classification_engine as classification
import data_pipeline.exception.exceptions as ex


class test_classify(unittest.TestCase):

    url = 'http://127.0.0.1:5000/classify'

    def test_response_200(self):
        request = requests.post(self.url, json=config)
        when2(classification.apply_classifier, config).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)

    '''def test_invalid_config(self):
        request = requests.post(self.url, json="Hallo")
        when2(classification.apply_classifier, config).thenReturn(ex.ConfigTypeException)
        response = request.status_code
        self.assertEqual(response, 900)
    '''

    def test_for_900(self):
        wrong_config = config.copy()
        del wrong_config['new_classifier_method']
        request = requests.post(self.url, json=config)
        when2(classification.apply_classifier, wrong_config).thenRaise(ex.ConfigTypeException)
        response = request.status_code
        self.assertEqual(response, 900)


    def test_for_901(self):
        pass

    def test_for_902(self):
        pass

    def test_for_90(self):
        pass


if __name__ == '__main__':
    unittest.main()
