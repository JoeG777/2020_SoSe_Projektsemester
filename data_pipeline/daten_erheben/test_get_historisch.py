import unittest
import data_pipeline.daten_erheben.get_historisch as his


class MyTestCase(unittest.TestCase):
    def test_get_timestamp_dwd(self):
        self.assertEqual(his.get_timestamp_dwd("202001050000"), "2020-01-05T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
