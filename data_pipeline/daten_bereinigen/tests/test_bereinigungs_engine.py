import unittest
from datetime import datetime
import data_pipeline.daten_bereinigen.src.bereinigungs_engine.bereinigungs_engine as be
import pandas as pd
import data_pipeline.exception.exceptions as exc

test_input = pd.Series({datetime.strptime("2020-01-20 23:07:02", "%Y-%m-%d %H:%M:%S"): 5.01})

#class test_format(unittest.TestCase):


#     def test_wrong_format_throws_exception(self):
#         test_data = pd.Series(["Hallo"])
#         self.assertRaises(exc.FormatException, be.format, test_data)
#
#     def test_format_works_correctly(self):
#         test_data = pd.Series([{'time': '2020-01-20T23:07:02.91667712Z', 'valueScaled': 5.01}])
#
#         datetime_obj = datetime.strptime("2020-01-20 23:07:02", "%Y-%m-%d %H:%M:%S")
#         expected_output = pd.Series({datetime_obj: 5.01})
#
#         self.assertEqual(be.format(test_data).all(), expected_output.all())
#
#     def test_format_empty_data_throws_exception(self):
#         self.assertRaises(exc.NoDataException, be.format, pd.Series({}, dtype="float64"))


class test_imputation(unittest.TestCase):
    test_data = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 02:01:00", "%Y-%m-%d %H:%M:%S"): 5.00})

    def test_low_threshold_throws_exception(self):
        self.assertRaises(exc.InvalidConfigValueException, be.imputation, test_imputation.test_data, -1)

    def test_imputation_works_correctly(self):
        timestamp1 = pd.Timestamp(datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"))
        timestamp2 = pd.Timestamp(datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"))

        expected_output = {'gap0': {'from': timestamp1, 'to': timestamp2}}
        self.assertEqual(expected_output, be.imputation(test_imputation.test_data, 3600))

    def test_imputation_no_gaps_works_correctly(self):
        test_data_no_gaps = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                       datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                       datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                       datetime.strptime("2020-01-20 00:03:00", "%Y-%m-%d %H:%M:%S"): 5.00})
        self.assertEqual(be.imputation(test_data_no_gaps, 3600), {})

    def test_imputation_empty_data_throws_exception(self):
        self.assertRaises(exc.NoDataException, be.imputation, pd.Series({}, dtype="float64"), 3600)


class test_rolling_mean(unittest.TestCase):
    test_data = pd.Series({datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 6.00,
                           datetime.strptime("2020-01-20 00:03:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                           datetime.strptime("2020-01-20 00:04:00", "%Y-%m-%d %H:%M:%S"): 8.00,
                           datetime.strptime("2020-01-20 00:05:00", "%Y-%m-%d %H:%M:%S"): 9.00})

    def test_small_framewidth_throws_exception(self):
        self.assertRaises(exc.InvalidConfigValueException, be.rolling_mean, test_rolling_mean.test_data, -1)

    def test_rolling_mean_works_correctly(self):
        expected_output = pd.Series({datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                                     datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                                     datetime.strptime("2020-01-20 00:03:00", "%Y-%m-%d %H:%M:%S"): 6.00,
                                     datetime.strptime("2020-01-20 00:04:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                                     datetime.strptime("2020-01-20 00:05:00", "%Y-%m-%d %H:%M:%S"): 8.00})

        self.assertEqual(be.rolling_mean(test_rolling_mean.test_data, 3).all(), expected_output.all())

    def test_rolling_mean_empty_data_throws_exception(self):
        self.assertRaises(exc.NoDataException, be.rolling_mean,  pd.Series({}, dtype="float64"), 100)


class test_resample(unittest.TestCase):
    test_data = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                           datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                           datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): 8.00,
                           datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 9.00})

    def test_resample_low_samplerate_throws_exception(self):
        self.assertRaises(exc.InvalidConfigValueException, be.resample, test_input, "0S")

    def test_resample_works_correctly(self):
        expected_output = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                     datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                                     datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 9.00})

        self.assertEqual(be.resample(test_resample.test_data, "60S").all(), expected_output.all())

    def test_resample_empty_data_throws_exception(self):
        self.assertRaises(exc.NoDataException, be.resample,  pd.Series({}, dtype="float64"), "60S")


class test_interpolation(unittest.TestCase):
    test_data = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                           datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                           datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                           datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                           datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                           datetime.strptime("2020-01-20 00:02:30", "%Y-%m-%d %H:%M:%S"): 9.00})

    def test_interpolation_works_correctly(self):
        expected_output = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                     datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                                     datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 6.2,
                                     datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): 6.3,
                                     datetime.strptime("2020-01-20 00:02:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                                     datetime.strptime("2020-01-20 00:02:30", "%Y-%m-%d %H:%M:%S"): 9.00})

        self.assertEqual(be.interpolation(test_interpolation.test_data).all(), expected_output.all())

    def test_interpolation_empty_data_throws_exception(self):
        self.assertRaises(exc.NoDataException, be.interpolation, pd.Series({}, dtype="float64"))


class test_remove_gaps(unittest.TestCase):


    timestamp1 = pd.Timestamp(datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"))
    timestamp2 = pd.Timestamp(datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"))
    imputation_dict = {'gap0': {'from': timestamp1, 'to': timestamp2}}

    def test_remove_gaps_works_with_empty_imputation_dict(self):
        test_data = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                               datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                               datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 6.2,
                               datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): 6.3,
                               datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                               datetime.strptime("2020-01-20 02:01:00", "%Y-%m-%d %H:%M:%S"): 9.00})
        #print(test_remove_gaps.test_data)

        self.assertEqual(be.remove_gaps(test_data, {}).all(), test_data.all())


    def test_remove_gaps_works_correctly(self):

        test_data = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                               datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                               datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): 6.2,
                               datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): 6.3,
                               datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"): 7.00,
                               datetime.strptime("2020-01-20 02:01:00", "%Y-%m-%d %H:%M:%S"): 9.00})


        expected_output = pd.Series({datetime.strptime("2020-01-20 00:00:00", "%Y-%m-%d %H:%M:%S"): 5.00,
                                     datetime.strptime("2020-01-20 00:00:30", "%Y-%m-%d %H:%M:%S"): 6.00,
                                     datetime.strptime("2020-01-20 00:01:00", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                                     datetime.strptime("2020-01-20 00:01:30", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                                     datetime.strptime("2020-01-20 02:00:00", "%Y-%m-%d %H:%M:%S"): float("NaN"),
                                     datetime.strptime("2020-01-20 02:01:00", "%Y-%m-%d %H:%M:%S"): 9.00})

        self.assertEqual(be.remove_gaps(test_data, test_remove_gaps.imputation_dict).all(), expected_output.all())

    def test_remove_gaps_empty_data_throws_exception(self):
        self.assertRaises(exc.NoDataException, be.remove_gaps,  pd.Series({}, dtype="float64"), test_remove_gaps.imputation_dict)


if __name__ == '__main__':
    unittest.main()
