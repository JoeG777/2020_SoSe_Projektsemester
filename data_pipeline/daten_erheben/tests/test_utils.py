import unittest
import data_pipeline.daten_erheben.src.utils.utils as util


class test_get_converted_date(unittest.TestCase):
    def test_timestamp_conversion(self):
        self.assertEqual(util.get_converted_date("2020-01-05T02:00:00Z"), "2020-01-05T01:00:00Z")


if __name__ == '__main__':
    unittest.main()
