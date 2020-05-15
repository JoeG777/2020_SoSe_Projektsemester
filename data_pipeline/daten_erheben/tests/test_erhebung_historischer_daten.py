import unittest
import data_pipeline.daten_erheben.src.erhebung_historischer_daten.erhebung_historischer_daten as his
from mockito import *
from mockito.matchers import ANY
import pandas as pd


class test_get_historic(unittest.TestCase):

    def test_raise_historic(self):
        # URL-Downloadlink
        url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/recent/10minutenwerte_TU_05906_akt.zip"

        # Array with weather-data
        return_data = []
        element1 = ["202001050000", "20"]
        element2 = ["202001060000", "20"]
        element3 = ["202001070000", "20"]
        return_data.append(element1)
        return_data.append(element2)
        return_data.append(element3)

        # JSON with formatted weather-data
        headers = ['time', 'temperature']
        data = [["2020-01-04T23:00:00Z", 20.0], ["2020-01-05T23:00:00Z", 20.0], ["2020-01-06T23:00:00Z", 20.0]]

        df = pd.DataFrame(data, columns=headers)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')

        when(his).get_temp_data(ANY).thenReturn(return_data)
        when(his).find_start_date(ANY).thenReturn(0)
        when(his).get_start_date().thenReturn("2020-01-05T00:00:00")
        when(his).write_into_tmp(ANY).thenReturn()

        pd.testing.assert_frame_equal(his.get_dwd_data(url), df, check_dtype=False)


if __name__ == '__main__':
    unittest.main()
