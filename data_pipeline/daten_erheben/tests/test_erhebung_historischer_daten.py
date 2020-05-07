import unittest
import data_pipeline.daten_erheben.src.erhebung_historischer_daten.erhebung_historischer_daten as his
import data_pipeline.exception.exceptions as exc


class MyTestCase(unittest.TestCase):
    def test_get_timestamp_dwd(self):
        self.assertEqual(his.get_timestamp_dwd("202001050000"), "2020-01-05T00:00:00Z")

    def test_get_temp_data(self):
        self.assertRaises(exc.UrlException, his.get_temp_data, '4r41.de')

    def test_raise_historic_data(self):
        self.assertRaises(exc.FileException, his.raise_historic_data, 'http://www.polyglotinc.com/resume/resumeXML.zip')

if __name__ == '__main__':
    unittest.main()
