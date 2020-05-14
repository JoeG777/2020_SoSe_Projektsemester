import unittest
from data_pipeline.daten_klassifizieren.classification_engine import convert_time
from data_pipeline.exception.exceptions import InvalidConfigValueException

class MyTestCase(unittest.TestCase):

    def test_invalid_value(self):
        invalid_config = {
            "timeframe": ["2020-01- 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
        }
        timeframe = invalid_config['timeframe']

        self.assertRaises(InvalidConfigValueException, convert_time, timeframe[0])

if __name__ == '__main__':
    unittest.main()
