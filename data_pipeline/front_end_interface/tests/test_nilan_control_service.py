import unittest
from datetime import datetime, timedelta
from data_pipeline.front_end_interface.src.nilan_control_service import nilan_control_service
import data_pipeline.exception.exceptions as exc


class test_nilan_control_serivce(unittest.TestCase):
    def test_get_current_time_utc(self):
        self.assertEqual(nilan_control_service.get_current_time_utc(), calculate_time())


    def test_format_json(self):

        json_nilan_array_1 = [
            {'measurement': 'raumtemperatur',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"temperatur": "Test"}
             },
            {'measurement': 'luefterstufe_zuluft',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"stufe": "Test"}
             },
            {'measurement': 'luefterstufe_abluft',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"stufe": "Test"}
             }
        ]

        json_nilan_array_2 = [
            {'measurement': 'raumtemperatur',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"temperatur": "Test"}
             },
            {'measurement': 'luefterstufe_zuluft',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"stufe": "Test"}
             },
            {'measurement': 'luefterstufe_abluft',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"stufe": "Test"}
             },
            {'measurement': 'betriebsmodus',
             "time": "2020-05-11T10:12:00Z",
             "fields": {"modus": "Test"}
             }
        ]

        compare = json_nilan_array_1 == json_nilan_array_2
        
        self.assertRaises(exc.RawDataException, compare_json_arrays(json_nilan_array_1, json_nilan_array_2))

def compare_json_arrays(json_1, json_2):

    try:
        json_1 == json_2

    except:
        raise exc.RawDataException('Not equal')

def calculate_time():

    time_now = datetime.now()
    time_difference = timedelta(hours=2)
    time_new = time_now - time_difference

    return str(time_new)[:10] + "T" + str(time_new)[11:19] + "Z"


if __name__ == '__main__':
    unittest.main()
