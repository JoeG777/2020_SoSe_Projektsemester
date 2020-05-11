import unittest
from data_pipeline.db_connector.src.write_manager import write_manager as wm


class test_build_write_json(unittest.TestCase):

    def test_adds_all_values(self):
        expected_json = [
            {'measurement': "test_measurement",
             "time": 1,
             "fields": {"test_value": 1.0}
             }
        ]

        output = wm.build_write_json("test_measurement", "1", "test_value", "1")

        self.assertEqual(expected_json, output)


if __name__ == '__main__':
    unittest.main()