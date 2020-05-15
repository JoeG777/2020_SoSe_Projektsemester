import unittest
from mockito import *
import requests
import data_pipeline.daten_erheben.src.data_collection_api.data_collection_api as dcapi


class test_data_collection_api(unittest.TestCase):

    config = {
        "historischURL": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/recent/10minutenwerte_TU_05906_akt.zip",
        "forecastURL": "https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/single_stations/10729/kml/MOSMIX_L_LATEST_10729.kmz"
    }

    url = "http://127.0.0.1:5000/forecast_datenerhebung"

    def test_response_200(self):
        request = requests.post(self.url, json=self.config)
        when2(dcapi.get_forecast_data).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)


if __name__ == "__main__":
    unittest.main()


