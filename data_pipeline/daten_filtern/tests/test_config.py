from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config
import unittest


class Filtern_engine_tests(unittest.TestCase):



    def test_all_curve(self):

        #expected_data
        expected_data = (["room","condenser","evaporator","inlet","outlet","freshAirIntake"])

        print(expected_data)

        #real_data

        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        #print(config)
        #real_data = filtern_config["filter_options"][filtern_config["selected_value"][filtern_config[""]]]
        real_data = config.keys()
        print(real_data)

        self.assertCountEqual(expected_data, expected_data)

    def test_cycle(self):

        config = filtern_config["filter_options"][filtern_config["selected_value"]]

        #expected_data
        expected_data = (["WarmWasserZyklus","OfenZyklus","LüfterZyklus","AbtauZyklus"])
        print(expected_data)

        #real_data
        real_data = config["room"].keys()
        print(real_data)

        self.assertCountEqual(expected_data, expected_data)


    def text_delete(self):

        config = filtern_config["filter_options"][filtern_config["selected_value"]]

        #expected_data
        expected_data = (["delete", "Interpolation"])
        print(expected_data)

        #real_data
        real_data = config["room"]["WarmWasserZyklus"].keys()
        print(real_data)

        self.assertCountEqual(expected_data, expected_data)

