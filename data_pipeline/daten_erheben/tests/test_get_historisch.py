import unittest
import data_pipeline.daten_erheben.src.get_historisch as his
from data_pipeline.daten_erheben.src.exception import url_exception


class MyTestCase(unittest.TestCase):
    def test_get_timestamp_dwd(self):
        self.assertEqual(his.get_timestamp_dwd("202001050000"), "2020-01-05T00:00:00Z")

    def test_get_temp_data(self):
        self.assertRaises(url_exception, his.get_temp_data, '4r41.de')

if __name__ == '__main__':
    unittest.main()
