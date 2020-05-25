import unittest
import pandas as pd
from mockito.matchers import ANY
from mockito import *
import copy
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from data_pipeline.daten_klassifizieren import trainingsdata_editing_engine as training
from data_pipeline.daten_klassifizieren import model_persistor as mp
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import data_pipeline.db_connector.src.write_manager.write_manager as wm
from data_pipeline.daten_klassifizieren.classification_engine import apply_classifier
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.exception.exceptions as ex
import data_pipeline.log_writer.log_writer as logger

when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))


class MyTestCase(unittest.TestCase):
    current_model_type_std = config['standard']
    model_dict = mp.load_dictionary('model_classification_engine.txt')
    df_test = rm.read_query('nilan_enriched', "SELECT * FROM standard WHERE time >= 1579225694062ms AND time <= 1579398691750ms")
    df_test_pred = rm.read_query('nilan_enriched', "SELECT * FROM pred WHERE time >= 1579225694062ms AND time <= 1579398691750ms")
    df_pred_test = rm.read_query('prediction_data', "SELECT * FROM vorhergesagteDaten WHERE time >= 1579225694062ms AND time <= 1579398691750ms")

    @classmethod
    def setUp(self):
        unstub()

    def test_valid_inputs(self):
        test_config = copy.deepcopy(config)

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(self.model_dict['abtauzyklus'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        self.assertEqual(apply_classifier(test_config), 0)

    def test_for_pred_classification(self):  # input shape for pred_classifier???
        test_config = copy.deepcopy(config)
        test_config['selected_event'] = 'pred'

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test_pred)
        when2(mp.load_classifier, ANY, 'abtauzyklus_pred').thenReturn(self.model_dict['abtauzyklus_pred'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung_pred').thenReturn(self.model_dict['warmwasseraufbereitung_pred'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        self.assertEqual(apply_classifier(test_config), 0)

    def test_config_of_wrong_type(self):
        test_config = 'Hallo'

        with self.assertRaises(ex.ConfigTypeException):
            apply_classifier(test_config)

    def test_for_fail_in_connector(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_enriched_data']['database'] = "Ich_bin_keine_database"
        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, "Ich_bin_keine_database", ANY).thenRaise(ex.DBException)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(self.model_dict['abtauzyklus'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        with self.assertRaises(ex.DBException):
            apply_classifier(test_config)

    def test_missing_entry_in_config(self):
        test_config = copy.deepcopy(config)
        del test_config['datasource_enriched_data']

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(self.model_dict['abtauzyklus'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        with self.assertRaises(ex.ConfigException):
            apply_classifier(test_config)

    def test_for_Index_error(self):
        pass

    def test_for_not_fitted_classifier(self):
        test_config = copy.deepcopy(config)

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(KNeighborsClassifier())
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        with self.assertRaises(ex.SklearnException):
            apply_classifier(test_config)

    def test_for_predicting_input_has_nans(self):
        test_config = copy.deepcopy(config)

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(self.model_dict['abtauzyklus'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, ANY)

        df_nan = self.df_test.copy()
        df_nan.iat[1, 1] = np.NaN
        when2(pd.DataFrame.copy).thenReturn(df_nan)

        with self.assertRaises(ex.SklearnException):
            apply_classifier(test_config)

    def test_writing_to_database_causes_exception(self):
        test_config = copy.deepcopy(config)
        test_config['datasource_classified_data']['measurement'] = "Kein_measurement"

        when2(training.enrich_data, ANY).thenReturn(0)
        when2(rm.read_query, ANY, ANY).thenReturn(self.df_test)
        when2(mp.load_classifier, ANY, 'abtauzyklus').thenReturn(self.model_dict['abtauzyklus'])
        when2(mp.load_classifier, ANY, 'warmwasseraufbereitung').thenReturn(self.model_dict['warmwasseraufbereitung'])
        when2(mp.persist_classifier, ANY, ANY, ANY)
        when2(wm.write_dataframe, ANY, ANY, 'Kein_measurement').thenRaise(ex.DBException)

        with self.assertRaises(ex.DBException):
            apply_classifier(test_config)


if __name__ == '__main__':
    unittest.main()
