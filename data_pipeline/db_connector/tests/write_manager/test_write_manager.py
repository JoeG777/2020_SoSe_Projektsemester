import unittest
import calendar
import time

from mock import ANY
from data_pipeline.db_connector.src.write_manager import write_manager as wm
from mockito.mockito import verify, when2, unstub


class test_write_single_value(unittest.TestCase):
    @classmethod
    def setUp(self):
        unstub()

    def test_writes_single_value_all_args(self):
        expected_json = {
            'measurement': "bar",
             "time": 1,
             "fields": {"my_val": 1.0}
             }

        when2(wm.write_query, "foo", expected_json).thenReturn(True)

        wm.write_single_value("foo",
                              "1.0",
                              measurement="bar",
                              value_name="my_val",
                              time_utc=1
                              )

        verify(wm).write_query("foo",
                               expected_json
                               )

    def test_writes_single_value_no_time(self):
        expected_json = {
            'measurement': "bar",
             "time": int(calendar.timegm(time.gmtime())),
             "fields": {"my_val": 1.0}
             }

        when2(wm.write_query, "foo", expected_json).thenReturn(True)

        wm.write_single_value("foo",
                              "1.0",
                              measurement="bar",
                              value_name="my_val"
                              )

        verify(wm).write_query("foo",
                               any
                               )


class write_multiple_values(unittest.TestCase):
    @classmethod
    def setUp(self):
        unstub()

    def test_writes_single_value_all_args(self):
        values = [1, 2]
        when2(wm.write_query, "foo", ANY).thenReturn(True)

        wm.write_multiple_values("foo",
                                 values,
                                 measurement=["bar", "bar"],
                                 value_name=["my_val", "my_val"]
                                 )
        verify(wm, 2).write_query("foo", any)

    def test_throws_exception(self):
        when2(wm.write_query, "foo", ANY).thenReturn(True)

        with self.assertRaises(ValueError):
            wm.write_multiple_values("foo", [1, 2], value_name=["my_val"])


if __name__ == '__main__':
    unittest.main()
