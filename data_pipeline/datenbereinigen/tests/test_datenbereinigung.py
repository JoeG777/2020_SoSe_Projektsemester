import unittest
from mockito import *
from mockito.matchers import ANY
import pandas as pd
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.datenbereinigen.src.bereinigungs_engine.bereinigungs_engine as be


class test_integration(unittest.TestCase):

    req_dummy = {
        'frame_width': 1,
        'freq': '1S',
        'register': "201"
        ,
        'time': {
            'from': '1579561622474ms',
            'to': '1580261128794ms'
        },
        'threshold': 3600,
    }

    read_data_mock = pd.Series([{'time': '2020-01-20T23:07:02.91667712Z', 'valueScaled': 5.01},
                      {'time': '2020-01-20T23:07:03.91667712Z', 'valueScaled': 5.01},
                      {'time': '2020-01-20T23:07:04.91667712Z', 'valueScaled': 5.01},
                      {'time': '2020-01-20T23:07:05.91667712Z', 'valueScaled': 5.01},
                      {'time': '2020-01-20T23:07:06.91667712Z', 'valueScaled': 5.01}])



    def test_valid_request(self):

        when2(read_manager.read_query, ANY, ANY, format=False).thenReturn(test_integration.read_data_mock)

        be.workflow("201",{"from": "1578268800189003008", "to": "1578392210340990976"},3600,1,"1S")
        #be.fast_and_furious("201", {"from": "1578268800189003008", "to": "1578392210340990976"}, 3600, 1, "1S")

        # send request to API
        #self.app = api.app.test_client()
        #resp = self.app.post('/datenbereinigung', json=test_integration.req_dummy)


