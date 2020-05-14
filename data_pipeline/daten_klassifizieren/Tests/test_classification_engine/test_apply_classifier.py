import unittest
import pandas as pd
import copy
from data_pipeline.daten_klassifizieren import trainingsdata_editing_engine as trainingsdata_editing_engine
from data_pipeline.daten_klassifizieren import model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
from data_pipeline.daten_klassifizieren.classification_engine import apply_classifier
from data_pipeline.daten_klassifizieren.config import classification_config as config
from data_pipeline.exception.exceptions import *
from mockito import *
from mockito.matchers import ANY

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        example_values = pd.DataFrame.from_dict({
            #"time": [1.0, 2.0, 3.0],
            "condenser": [17.0, 17.0, 17.0],
            "evaporator": [17.0, 17.0, 17.0],
            "freshAirIntake": [13.0, 34.2, 34.0],
            "inlet": [99.2, 91.2, 192.2],
            "outlet": [17.0, 17.0, 17.0],
            "room": [13.2, 61.2, 02.3],
            'evaporator_deriv': [17.0, 17.0, 17.0],
            'evaporator_pct_ch': [17.0, 17.0, 17.0],
            'evaporator_ch_abs': [17.0, 17.0, 17.0],
            'evaporator_diff': [17.0, 17.0, 17.0],
            'condenser_deriv': [17.0, 17.0, 17.0],
            'condenser_pct_ch': [17.0, 17.0, 17.0],
            'condenser_ch_abs': [17.0, 17.0, 17.0],
            'condenser_diff': [17.0, 17.0, 17.0]
        })
        self.example_df = example_values

    def test_apply_classifier(self):
        train_config = copy.deepcopy(config)
        train_config['datasource_classifier'] = 'model.txt'
        model = model_persistor.load_classifier(train_config)
        when2(trainingsdata_editing_engine.enrich_data, config).thenReturn(0)
        when2(read_manager.read_query, ANY, ANY).thenReturn(self.example_df)
        when2(model_persistor.load_classifier, config).thenReturn(model)
        when2(write_manager.write_dataframe, ANY, ANY, ANY)

        self.assertEqual(apply_classifier(train_config),0)

    def test_not_fitted_classifier(self):
        train_config = config.copy()
        train_config['datasource_classifier'] = 'model_test_returns_existing_classifier.txt'
        model = model_persistor.load_classifier(train_config)
        when2(trainingsdata_editing_engine.enrich_data, config).thenReturn(0)
        when2(read_manager.read_query, ANY, ANY).thenReturn(self.example_df)
        when2(model_persistor.load_classifier, config).thenReturn(model)
        when2(write_manager.write_dataframe, ANY, ANY, ANY).thenReturn(0)

        self.assertRaises(SklearnException, apply_classifier, train_config)



if __name__ == '__main__':
    unittest.main()
