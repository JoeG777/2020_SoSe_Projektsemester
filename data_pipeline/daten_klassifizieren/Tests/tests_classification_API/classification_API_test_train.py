import unittest
import requests
import copy
from mockito import *
from mockito.matchers import ANY

import data_pipeline.exception as ex
import data_pipeline.daten_klassifizieren.classification_engine as classification
from data_pipeline.daten_klassifizieren.config import classification_config as config


class test_train(unittest.TestCase):
    url = 'http://127.0.0.1:5000/train'

    def test_response_200(self):
        print("Tests sind geil!")
        spy2(classification.apply_classifier)
        request = requests.post(self.url, json={"Hallo": "ich bin ein Request"})
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 200)

'''
    def test_invalid_config(self):
        request = requests.post(self.url, json="Hallo")
        response = request.status_code
        self.assertEqual(response, 500)

    def test_for_900(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['new_classifier_method']
        request = requests.post(self.url, json=wrong_config)

        when2(classification.apply_classifier, wrong_config).thenRaise(ex.ConfigTypeException)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_for_901(self):
        request = requests.post(self.url, json=config)

        when2(classification.apply_classifier, config).thenThrow(ex.DBException)
        response = request.status_code
        self.assertEqual(response, 901)

    def test_for_902(self):
        test_config = copy.deepcopy(config)
        test_config['selected_event'] = 'ofennutzung'
        request = requests.post(self.url, json=test_config)

        # when2(classification.apply_classifier, ANY).thenRaise(ex.PersistorException)
        response = request.status_code
        self.assertEqual(response, 902)

    def test_for_903(self):
        pass
'''


def main():
    unittest.main()


# if __name__ == '__main__':
    # unittest.main()
