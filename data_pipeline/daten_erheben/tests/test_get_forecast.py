import unittest
import data_pipeline.daten_erheben.src.forecast_data.get_forecast as fore
from data_pipeline.daten_erheben.src.exception import UrlException



class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertRaises(UrlException, fore.get_forecast, 'ungueltige_url')

if __name__ == '__main__':
    unittest.main()
