import unittest
from mockito import mockito
from mockito.mockito import when
from data_pipeline.db_connector.src.read_manager import read_manager as rm
from influxdb import InfluxDBClient
from influxdb import DataFrameClient


class test_build_write_json(unittest.TestCase):

    def test_adds_all_values(self):
        mock_client = mockito.Mock(InfluxDBClient)
        when(mock_client).query(any()).thenReturn("test")

        output = rm.build_write_json("test_measurement", "1", "test_value", "1")

        self.assertEqual(expected_json, output)


if __name__ == '__main__':
    unittest.main()