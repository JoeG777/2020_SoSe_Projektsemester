import unittest
import data_pipeline.daten_erheben.src.erhebung_vorhersagedaten.erhebung_vorhersagedaten as fore
from data_pipeline.exception.exceptions import UrlException, FileException


class test_get_forecast(unittest.TestCase):
    def test_something(self):
        self.assertRaises(UrlException, fore.get_forecast, 'ungueltige_url')


class test_raise_forecast_data(unittest.TestCase):
    def test_something(self):
        self.assertRaises(UrlException, fore.raise_forecast_data, 'ungueltige_url')


class text(unittest.TestCase):
    def test_something(self):
        self.assertRaises(FileException, fore.get_forecast_data, 'https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_LATEST.kmz')


if __name__ == '__main__':
    unittest.main()
