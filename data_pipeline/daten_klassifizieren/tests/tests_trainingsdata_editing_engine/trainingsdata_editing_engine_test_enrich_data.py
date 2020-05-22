import pandas as pd
from mockito import *
from mockito.matchers import ANY, captor
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn(mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
                                                                  error=lambda x: print(x), write_into_measurement=
                                                                  lambda x: print(x))))
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import unittest
from data_pipeline.exception.exceptions import *
import copy


class test_enrich_data(unittest.TestCase):
    @classmethod
    def setUp(self):
        unstub()

    def test_key_missing_in_config(self):
        wrong_config = copy.deepcopy(config)
        wrong_config.pop('selected_event')
        self.assertRaises(InvalidConfigKeyException, trainingsdata.enrich_data, wrong_config)

    def test_end_time_wrong_format(self):
        wrong_config = copy.deepcopy(config)
        wrong_config['timeframe'][1] = '2020.10.10'
        self.assertRaises(InvalidConfigValueException, trainingsdata.enrich_data, wrong_config)


    def test_register_name_not_in_df_column(self):
        spy2(read_manager.read_data)
        wrong_config = copy.deepcopy(config)
        wrong_config['selected_event'] = 'standard'
        df_query = pd.DataFrame.from_dict({
            "time": [1.0, 2.0, 3.0],
            "inlet": [99.2, 91.2, 192.2],
            "room": [13.2, 61.2, 02.3],
            "freshAirIntake": [13.0, 34.2, 34.0],
            "condr": [17.0, 17.0, 17.0],
            "evaporator": [17.0, 17.0, 17.0],
            "outlet": [17.0, 17.0, 17.0]})
        df_query["time"] = pd.to_datetime(df_query["time"])
        df_query = df_query.set_index("time")
        when2(read_manager.read_query, ANY, ANY).thenReturn(df_query)
        self.assertRaises(InvalidConfigValueException, trainingsdata.enrich_data, wrong_config)

    def test_enriched_dataframe_has_correct_format(self):
        test_config = config.copy()
        test_config['selected_event'] = 'standard'
        example_df = pd.DataFrame.from_dict({
            "time": [1.0, 2.0, 3.0],
            "outdoor": [14.2, 4.1, 1.32],
            "inlet": [99.2, 91.2, 192.2],
            "room": [13.2, 61.2, 02.3],
            "freshAirIntake": [13.0, 34.2, 34.0],
            "condenser": [17.0, 17.0, 17.0],
            "evaporator": [17.0, 17.0, 17.0],
            "outlet": [17.0, 17.0, 17.0]})
        example_df["time"] = pd.to_datetime(example_df["time"])
        example_df = example_df.set_index("time")
        enriched_df = pd.DataFrame.from_dict({
            "time": [1.0, 2.0, 3.0],
            "outdoor": [14.2, 4.1, 1.32],
            "inlet": [99.2, 91.2, 192.2],
            "room": [13.2, 61.2, 02.3],
            "freshAirIntake": [13.0, 34.2, 34.0],
            "condenser": [17.0, 17.0, 17.0],
            "evaporator": [17.0, 17.0, 17.0],
            "outlet": [17.0, 17.0, 17.0],
            'evaporator_deriv': [17.0, 17.0, 17.0],
            'evaporator_pct_ch': [17.0, 17.0, 17.0],
            'evaporator_ch_abs': [17.0, 17.0, 17.0],
            'evaporator_diff': [17.0, 17.0, 17.0],
            'condenser_deriv': [17.0, 17.0, 17.0],
            'condenser_pct_ch': [17.0, 17.0, 17.0],
            'condenser_ch_abs': [17.0, 17.0, 17.0],
            'condenser_diff': [17.0, 17.0, 17.0],
            'room_deriv': [17.0, 17.0, 17.0],
            'room_pct_ch': [17.0, 17.0, 17.0],
            'room_ch_abs': [17.0, 17.0, 17.0],
            'room_diff': [17.0, 17.0, 17.0],
            'inlet_deriv': [17.0, 17.0, 17.0],
            'inlet_pct_ch': [17.0, 17.0, 17.0],
            'inlet_ch_abs': [17.0, 17.0, 17.0],
            'inlet_diff': [17.0, 17.0, 17.0]
        })

        enriched_df["time"] = pd.to_datetime(enriched_df["time"])
        enriched_df = enriched_df.set_index("time")
        when2(read_manager.read_query, ANY, ANY).thenReturn(example_df)
        df_captor = captor(any(pd.DataFrame))
        when2(write_manager.write_dataframe, ANY, df_captor, ANY)
        trainingsdata.enrich_data(test_config)
        df = df_captor.value
        self.assertListEqual(df.columns.tolist(), enriched_df.columns.tolist())