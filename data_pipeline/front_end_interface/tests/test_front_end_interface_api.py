import unittest
from mockito import *
import requests
import data_pipeline.front_end_interface_old.src.front_end_interface_api.front_end_interface_api as feiapi


class test_data_collection_api(unittest.TestCase):

    config = {
        "start_datum": "2020-05-05T23:00:00Z",
        "end_datum": "2020-05-05T23:00:00Z",
        "vorhersage": "1",
        "raumtemperatur": "20.0",
        "luefterstufe_zuluft": "1",
        "luefterstufe_abluft": "1",
        "betriebsmodus": "2"
    }

    config_wrong = {
        "start_dwdatum": "2020-05-05T23:00:00Z",
        "end_datdwdum": "2020-05-05T23:00:00Z",
        "vorhedwrsage": "1",
        "raumdwtemperatur": "20.0",
        "luefwdterstufe_zuluft": "1",
        "lueftwderstufe_abluft": "1",
        "betriwdebsmodus": "2"
    }

    url = "http://127.0.0.1:5000/nilan_control_service"

    def test_response_200(self):
        request = requests.post(self.url, json=self.config)
        response = request.status_code
        self.assertEqual(response, 200)

    def test_response_900_wrong_config(self):
        request = requests.post(self.url, json=self.config_wrong)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_empty_config(self):
        request = requests.post(self.url, json={})
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_string(self):
        request = requests.post(self.url, "json={}")
        response = request.status_code
        self.assertEqual(response, 900)


if __name__ == "__main__":
    unittest.main()
