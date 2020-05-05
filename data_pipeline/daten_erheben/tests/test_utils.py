import unittest
import data_pipeline.daten_erheben.src.utils as util


class MyTestCase(unittest.TestCase):
    def test_get_converted_date(self):
        self.assertEqual(util.get_converted_date("2020-01-05T02:00:00Z"), "2020-01-05T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
