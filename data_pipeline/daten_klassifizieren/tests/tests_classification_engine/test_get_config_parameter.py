import unittest
from mockito.matchers import ANY
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))
from data_pipeline.daten_klassifizieren.classification_engine import get_config_parameter
from data_pipeline.exception.exceptions import ConfigException

class MyTestCase(unittest.TestCase):

    def test_missing_config_parameter(self):
        incomplete_config = {
            #"datasource_raw_data": {'database': 'nilan_cleaned', 'measurement': 'temperature_register'},
            "datasource_enriched_data": {'database': 'nilan_enriched', 'measurement': 'training'},
            "datasource_classified_data": {'database': 'nilan_classified', 'measurement': 'classified'},
            "timeframe": ["2020-01-14 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
            "selected_event": "abtauzyklus",
            "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                              "206": "evaporator"},
        }
        self.assertRaises(ConfigException, get_config_parameter, incomplete_config)

    def test_invalid_config_parameter(self):
        invalid_config = {
            "datasource_raw_data": {'database': 'nilan_cleaned', 'measurement': 'temperature_register'},
            "datasource_enriched_data": {'database': 'nilan_enriched', 'measurement': 'training'},
            "datasource_classified_data": {},
            "timeframe": ["2020-01-14 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
            "selected_event": "abtauzyklus",
            "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                              "206": "evaporator"},
        }
        self.assertRaises(ConfigException, get_config_parameter, invalid_config)


if __name__ == '__main__':
    unittest.main()
