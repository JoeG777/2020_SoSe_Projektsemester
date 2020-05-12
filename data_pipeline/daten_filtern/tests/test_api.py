import unittest
import data_pipeline.daten_filtern.src.filtern_api.filtern_api as api

class test_api(unittest.TestCase):

    def test_empty_request(self):
        self.app = api.app.test_client()
        resp = self.app.post('/filtern')
        self.assertEqual(resp , 200)