import unittest
import data_pipeline.daten_filtern.src.filtern_api.filtern_api as api
import requests
from mockito import *


class test_api(unittest.TestCase):

    url = "127.0.0.1:5000/filtern"
    config =
#def test_empty_request(self):
    #self.app = api.app.test_client()
    #resp = self.app.post('/filtern')
    #self.assertEqual(resp , 200)

def test_response_200(self):

    request = requests.post(self.url, json = self.config)