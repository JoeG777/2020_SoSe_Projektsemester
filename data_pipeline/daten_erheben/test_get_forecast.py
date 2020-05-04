import unittest
import data_pipeline.daten_erheben.get_forecast as fore
from data_pipeline.daten_erheben.exception import file_exception, url_exception, raw_data_exception

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertRaises(url_exception, get_forecast, 'ungueltige_url')

if __name__ == '__main__':
    unittest.main()
