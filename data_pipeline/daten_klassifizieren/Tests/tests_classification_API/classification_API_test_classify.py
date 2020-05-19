import copy
import unittest
from mockito.matchers import ANY, captor
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))
import requests


import data_pipeline.exception.exceptions as ex
from data_pipeline.daten_klassifizieren import classification_engine as classification
from data_pipeline.daten_klassifizieren.config import classification_config as config
from data_pipeline.db_connector.src.read_manager import read_manager


class test_classify(unittest.TestCase):
    url = 'http://127.0.0.1:5000/classify'

    @classmethod
    def setUp(cls):
        unstub()
        spy2(classification.apply_classifier)

    def test_response_200_with_abtauzyklus(self):
        when2(classification.apply_classifier, ANY).thenReturn(0)

        request = requests.post(self.url, json=config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 200)

    def test_invalid_config(self):
        when2(classification.apply_classifier, ANY).thenRaise(ex.ConfigTypeException)

        request = requests.post(self.url, json="Hallo")
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_for_900(self):
        when2(classification.apply_classifier, ANY).thenRaise(ex.ConfigTypeException)
        wrong_config = config.copy()
        del wrong_config['new_classifier_method']

        request = requests.post(self.url, json=wrong_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_for_901(self):
        when2(classification.apply_classifier, ANY).thenRaise(ex.DBException)

        request = requests.post(self.url, json=config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 901)

    def test_for_902(self):
        test_config = copy.deepcopy(config)
        test_config['selected_event'] = 'ofennutzung'
        when2(classification.apply_classifier, ANY).thenRaise(ex.PersistorException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 902)

    def test_for_903(self):
        pass

    def test_datasource_raw_data_missing(self):
        test_config = copy.deepcopy(config)
        del test_config['datasource_raw_data']
        when2(classification.apply_classifier, ANY).thenRaise(ex.InvalidConfigKeyException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_datasource_raw_data_None(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = None
        when2(classification.apply_classifier, ANY).thenRaise(ex.InvalidConfigValueException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_datasource_raw_data_wrong_type(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = "Hallo, ich bin keine Datenbank"
        when2(classification.apply_classifier, ANY).thenRaise(ex.InvalidConfigValueException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_datasource_raw_data_database_not_existing(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = {'database': 'ich_existiere_nicht', 'measurement': 'temperature'}
        when2(classification.apply_classifier, ANY).thenRaise(ex.DBException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 901)

    def test_datasource_raw_data_measurement_missing(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_raw_data'] = {'database': 'test'}
        when2(classification.apply_classifier, ANY).thenRaise(ex.ConfigException)

        request = requests.post(self.url, json=test_config)
        response = request.status_code

        verify(classification).apply_classifier(ANY)
        self.assertEqual(response, 900)

    def test_datasource_classifier_missing(self):
        pass

    def test_datasource_classifier_none(self):
        pass

    def test_datasource_classifier_empty(self):
        pass

    def test_datasource_classifier_wrong_file(self):
        pass

    def test_datasource_classifier_unpicklable(self):
        pass

    def test_datasource_classifier_missing(self):
        pass


if __name__ == '__main__':
    unittest.main()
