import unittest
from mockito import mockito, ANY, mock
from mockito.matchers import Any
from mockito.mockito import when2, verify
from data_pipeline.db_connector.src.read_manager import read_manager as rm
from data_pipeline.db_connector.src.read_manager.read_manager import format_data as fd
from influxdb import InfluxDBClient
from influxdb import DataFrameClient


class test_build_write_json(unittest.TestCase):

    def test_adds_all_values(self):
        #mock_client = mock(InfluxDBClient())
        #when2(InfluxDBClient.__init__(mock_client, "localhost", 8086, "admin", "admin")).thenReturn(mock_client)
        when2(InfluxDBClient.query).thenReturn(None)
        #when2(rm.format_data, "test").thenReturn("success!")

        output = rm.read_query("test", "test_measurement")

        self.assertEqual(output, "success!")


if __name__ == '__main__':
    unittest.main()