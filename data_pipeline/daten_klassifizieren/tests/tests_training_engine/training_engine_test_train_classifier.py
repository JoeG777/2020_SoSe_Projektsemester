import copy
import unittest
import pandas as pd
import sklearn
from sklearn import model_selection, neighbors
from mockito.matchers import ANY
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))

import data_pipeline.exception.exceptions as ex
import data_pipeline.daten_klassifizieren.training_engine as training_engine
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import data_pipeline.daten_klassifizieren.model_persistor as mp
from data_pipeline.daten_klassifizieren.config import classification_config as config


class TestTrainClassifier(unittest.TestCase):
    model = neighbors.KNeighborsClassifier()

    @classmethod
    def setUp(self):
        unstub()
        df = pd.DataFrame.from_dict({
            "time": ["1970-01-01 00:00:00.000", "1970-01-01 01:00:00.000", "1970-01-01 02:00:00.000"], "values":[1.0, 2.0, 3.0]})
        df['time'] = pd.to_datetime(df['time'])
        self.df_wrong = df.set_index('time')

        df_normal = pd.DataFrame.from_dict({
            "time": ["2020-01-14 10:41:00+00:00", "2020-01-17 03:55:00+00:00", "2020-01-17 06:56:00+00:00"],
            "abtauzyklus":[-1.0, 1.0, 0.0],
            "abtauzyklus_marker":[1.0, 1.0, 0.0],
            "warmwasseraufbereitung":[-1.0, 1.0, 0.0],
            "warmwasseraufbereitung_marker":[1.0, 1.0, 0.0]})
        df_normal['time'] = pd.to_datetime(df_normal['time'])
        self.df_normal = df_normal.set_index('time')

    def test_successful(self):
        pass

    def test_selected_event_deleted(self):
        wrong_config = copy.deepcopy(config)
        del wrong_config['selected_event']

        self.assertRaises(ex.InvalidConfigValueException, training_engine.train_classifier, wrong_config)

    def test_start_time_is_empty_throws_InvalidConfigValue(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['timeframe'] = ["2020-02-28 00:00:00.000 UTC", "2020-02-31 00:00:00.000 UTC" ]

        with self.assertRaises(ex.InvalidConfigValueException):
            training_engine.train_classifier(wrong_config)

    def test_no_trainingsdata_time_points_for_timeframe(self):
        wrong_config = copy.deepcopy(config)

        when2(rm.read_query, ANY, ANY).thenReturn(self.df_wrong)

        with self.assertRaises(ex.ConfigException):
            training_engine.train_classifier(wrong_config)

    def test_raise_persistor_exception(self):
        wrong_config = copy.deepcopy(config)

        when2(rm.read_query, ANY, ANY).thenReturn(self.df_normal)
        when2(mp.load_classifier, ANY, ANY, True).thenRaise(ex.PersistorException)

        with self.assertRaises(ex.PersistorException):
            training_engine.train_classifier(wrong_config)

    def test_train_test_split_SKlearnException(self):
        wrong_config = copy.deepcopy(config)

        when2(rm.read_query, ANY, ANY).thenReturn(self.df_normal)
        when2(mp.load_classifier, ANY, ANY, True).thenReturn(self.model)

        with self.assertRaises(ex.SklearnException):
            training_engine.train_classifier(wrong_config)

    def test_fit_SKlearnException(self):
        wrong_config = copy.deepcopy(config)

        when2(rm.read_query, ANY, ANY).thenReturn(self.df_normal)
        when2(mp.load_classifier, ANY, ANY, True).thenReturn(self.model)
        when2(sklearn.model_selection.train_test_split, ANY, ANY, test_size=ANY).thenReturn(None, None, None, None)

        with self.assertRaises(ex.SklearnException):
            training_engine.train_classifier(wrong_config)

    def test_model_not_persisted(self):
        pass

        '''
        wrong_config = copy.deepcopy(config)
        spy2(mp.persist_classifier)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_normal)
        when2(mp.load_classifier, ANY, ANY, True).thenReturn(self.model)
        when2(model_selection.train_test_split, ANY, ANY).thenReturn(None, None, None, None)
        when2(self.model.fit, ANY, ANY).thenReturn(self.model)
        when2(training_engine.evaluate_classifier, ANY, ANY, ANY, ANY).thenReturn(False)

        verify(mp, times(0)).persist_classifier(ANY, ANY, ANY)
        self.assertEqual(training_engine.train_classifier(wrong_config), 0)
        '''

if __name__ == '__main__':
    unittest.main()
