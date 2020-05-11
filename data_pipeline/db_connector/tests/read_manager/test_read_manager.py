import unittest
import pandas

from influxdb.resultset import ResultSet
from mockito.mockito import when2, unstub
from data_pipeline.db_connector.src.read_manager import read_manager as rm
from influxdb import InfluxDBClient


class test_read_query(unittest.TestCase):
    @classmethod
    def setUp(self):
        unstub()

    def test_adds_all_values(self):
        test_result_set = ResultSet({
            "time": 1,
            "message": "success!"
        })
        when2(test_result_set.get_points).thenReturn({
            "time": 1,
            "message": "success!"
        })
        test_dataframe = pandas.DataFrame({'time': [1], 'message': ['success!']})
        when2(InfluxDBClient.query, "test_measurement").thenReturn(test_result_set)
        when2(pandas.DataFrame, {"time": 1, "message": "success!"}).thenReturn(test_dataframe)

        output = rm.read_query("test", "test_measurement")

        self.assertEqual(len(output["message"]), 1)
        self.assertTrue("success!" in output["message"]["1970-01-01 00:00:00.000000001"])


class test_read_data(unittest.TestCase):
    @classmethod
    def setUp(self):
        unstub()

    def test_all_values_in_args(self):
        expected_query = "select from test_measurement where register = '201' AND time > 1ms AND time < 2ms"
        when2(rm.read_query, "test", expected_query).thenReturn("success!")

        output = rm.read_data("test",
                     measurement="test_measurement",
                     register="freshAirIntake",
                     resolve_register="True",
                     start_utc=1,
                     end_utc=2
                     )

        self.assertEqual(output, "success!")

    def test_no_time_set(self):
        expected_query = "select from test_measurement where register = '201'"
        when2(rm.read_query, "test", expected_query).thenReturn("success!")

        output = rm.read_data("test",
                            measurement="test_measurement",
                            register="freshAirIntake",
                            resolve_register="True"
                            )

        self.assertEqual(output, "success!")

    def test_only_start_set(self):
        expected_query = "select from test_measurement where register = '201' AND time > 1ms"
        when2(rm.read_query, "test", expected_query).thenReturn("success!")

        output = rm.read_data("test",
                              measurement="test_measurement",
                              register="freshAirIntake",
                              resolve_register="True",
                              start_utc=1
                              )

        self.assertEqual(output, "success!")

    def test_only_end_set(self):
        expected_query = "select from test_measurement where register = '201' AND time < 1ms"
        when2(rm.read_query, "test", expected_query).thenReturn("success!")

        output = rm.read_data("test",
                              measurement="test_measurement",
                              register="freshAirIntake",
                              resolve_register="True",
                              end_utc=1
                              )

        self.assertEqual(output, "success!")

    def test_do_not_resolve_register(self):
        expected_query = "select from test_measurement where register = 'freshAirIntake'"
        when2(rm.read_query, "test", expected_query).thenReturn("success!")

        output = rm.read_data("test",
                              measurement="test_measurement",
                              register="freshAirIntake"
                              )

        self.assertEqual(output, "success!")


if __name__ == '__main__':
    unittest.main()