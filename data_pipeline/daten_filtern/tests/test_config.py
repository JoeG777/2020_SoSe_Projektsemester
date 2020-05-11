from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config
import data_pipeline.daten_filtern.src.filtern_engine.filtern_engine as fe
import unittest
import pandas as pd

class Filtern_engine_tests(unittest.TestCase):

    def test_all_curve(self):

        #expected_data
        expected_x = range(0,6)
        expected_data = pd.Series(["room","condenser","evaporator","inlet","outlet","freshAirIntake"] , index = expected_x)


        #real_data
        real_data = filtern_config["filter_options"][filtern_config["selected_value"]]

        self.assertEqual(real_data.all() , expected_data.all())