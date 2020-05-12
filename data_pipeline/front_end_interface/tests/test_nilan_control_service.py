import unittest
import data_pipeline.front_end_interface.src.nilan_control_service.nilan_control_service as ncs

class MyTestCase(unittest.TestCase):
    def get_current_time_utc(self):
        self.assertEqual(ncs.get_current_time_utc("2020-01-05T02:00:00Z"), "2020-01-05T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
