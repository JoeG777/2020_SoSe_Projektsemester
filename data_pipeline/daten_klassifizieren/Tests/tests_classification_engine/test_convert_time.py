import unittest
from mockito.matchers import ANY
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))
from data_pipeline.daten_klassifizieren.classification_engine import convert_time
from data_pipeline.exception.exceptions import InvalidConfigValueException

class MyTestCase(unittest.TestCase):

    def test_invalid_value(self):
        invalid_config = {
            "timeframe": ["2020-01- 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
        }
        timeframe = invalid_config['timeframe']

        self.assertRaises(InvalidConfigValueException, convert_time, timeframe[0])

    def test_missing_value(self):
        invalid_config = {
            "timeframe": [""],
        }
        timeframe = invalid_config['timeframe']

        self.assertRaises(InvalidConfigValueException, convert_time, timeframe[0])

    def test_valid_value(self):
        invalid_config = {
            "timeframe": ["2020-01-14 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
        }
        timeframe = invalid_config['timeframe']

        self.assertEqual(convert_time(timeframe[0]), 1578956400000)

if __name__ == '__main__':
    unittest.main()
