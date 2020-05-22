import unittest
import data_pipeline.daten_erheben.src.erhebung_historischer_daten.erhebung_historischer_daten as his
import data_pipeline.exception.exceptions as exc


class test_get_timestamp_dwd(unittest.TestCase):
    def test_timestamp_conversion(self):
        self.assertEqual(his.get_timestamp_dwd("202001050000"), "2020-01-05T00:00:00Z")


class test_get_temp_data(unittest.TestCase):
    def test_with_invalid_url(self):
        self.assertRaises(exc.UrlException, his.get_temp_data, '4r41.de')


class test_raise_historic_data(unittest.TestCase):
    def test_with_invalid_url(self):
        self.assertRaises(exc.UrlException, his.raise_historic_data, 'jefnoeo.de')

    def test_with_invalid_xml_file(self):
        self.assertRaises(exc.FileException, his.raise_historic_data, 'http://www.polyglotinc.com/resume/resumeXML.zip')


if __name__ == '__main__':
    unittest.main()
