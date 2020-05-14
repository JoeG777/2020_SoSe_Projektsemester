import unittest
import data_pipeline.daten_filtern.src.filtern_engine.filtern_engine as fe
import pandas as pd
import numpy as np

from mockito import *
from mockito.matchers import ANY
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager

class Filtern_engine_tests(unittest.TestCase):
    def test_tag_drop(self):
        #opening_data
        opening_y = range(0,10)
        opening_time = pd.Series([10 ,11,12,13,14,15,16,17,18,19])
        opening_room = pd.Series([1,2,3,4,5,6,7,8,9,10] , index = opening_y)
        opening_ofen_zyklus = pd.Series([False, False, False, True, True, True, True, False, True, False], index = opening_y)
        opening_data = pd.concat([opening_time, opening_room, opening_ofen_zyklus], axis = 1)
        opening_namen = ["time" , "room" , "OfenZyklus"]
        opening_data.columns = opening_namen
        opening_data = opening_data.set_index("time")


        #expected_data
        expected_y = range(0,10)
        expected_time = pd.Series([10 ,11,12,13,14,15,16,17,18,19])
        expected_room = pd.Series([1,2,3,np.NaN, np.NaN, np.NaN, np.NaN, 8 , np.NaN, 10] , index = expected_y)
        expected_ofen_zyklus = pd.Series([False, False, False, True, True, True, True, False, True, False], index = expected_y)
        expected_data = pd.concat([expected_time, expected_room, expected_ofen_zyklus], axis = 1)
        expected_namen = ["time" , "room" , "OfenZyklus"]
        expected_data.columns = expected_namen
        expected_data = expected_data.set_index("time")

        #real_data
        real_data = fe.tag_drop('room' , 'OfenZyklus' , opening_data)

        #comparison real_data and exected_data
        self.assertEqual(real_data.room.all() , expected_data.room.all())




    def test_interpolation(self):
        #opening_data
        opening_y = range(0,10)
        opening_time = pd.Series([10 ,11,12,13,14,15,16,17,18,19])
        opening_room = pd.Series([1,2,3,np.NaN, np.NaN, np.NaN, np.NaN, 8 , np.NaN, 10] , index = opening_y)
        opening_ofen_zyklus = pd.Series([False, False, False, True, True, True, True, False, True, False], index = opening_y)
        opening_data = pd.concat([opening_time, opening_room, opening_ofen_zyklus], axis = 1)
        opening_namen = ["time" , "room" , "OfenZyklus"]
        opening_data.columns = opening_namen
        opening_data = opening_data.set_index("time")

        #expected_data
        expected_y = range(0,10)
        expected_time = pd.Series([10 ,11,12,13,14,15,16,17,18,19])
        expected_room = pd.Series([1,2,3,4,5,6,7,8,9,10] , index = expected_y)
        expected_ofen_zyklus = pd.Series([False, False, False, True, True, True, True, False, True, False], index = expected_y)
        expected_data = pd.concat([expected_time, expected_room, expected_ofen_zyklus], axis = 1)
        expected_namen = ["time" , "room" , "OfenZyklus"]
        expected_data.columns = expected_namen
        expected_data = expected_data.set_index("time")

        #real_data
        real_data = fe.interpolation("linear", "room", opening_data)

        #comparison real_data and exected_data
        self.assertEqual(real_data.room.all() , expected_data.room.all())


    # klassififcate
    temperature_data = {
        "time": [1, 2, 3, 4, 5, 6, 7],
        "valueScaled": [2, 4, 6, 8, 10, 12, 14]
    }
"""
    klassificate_dataframe = pd.DataFrame(temperature_data)

    # spies
    spy2(read_manager.read_data)
    spy2(write_manager.write_dataframe)

    # when the function tries to get the klassified data from database, return the custom klassified DataFrame above
    when2(read_manager.read_data, ANY, measurement=ANY, register=ANY).thenReturn(klassificate_dataframe)

    # verify all interactions (default times is 1)
    verify(read_manager).read_data(ANY, measurement=ANY, register=ANY)
    verify(write_manager).write_dataframe(ANY, ANY, ANY)
"""

if __name__ == '__main__':
    unittest.main()
