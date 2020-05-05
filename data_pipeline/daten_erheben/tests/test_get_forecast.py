import unittest
from data_pipeline.daten_erheben.src.exception import url_exception


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertRaises(url_exception, get_forecast, 'ungueltige_url')

if __name__ == '__main__':
    unittest.main()
