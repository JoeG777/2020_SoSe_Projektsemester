import unittest
import data_pipeline.front_end_interface.src.nilan_control_service as ncs
from datetime import datetime, timedelta

class MyTestCase(unittest.TestCase):
    def get_current_time_utc(self):
        self.assertEqual(ncs.get_current_time_utc(), calculate_time())

def calculate_time():

    time_now = datetime.now()
    time_difference = timedelta(hours=2)
    time_new = time_now - time_difference

    return time_new

if __name__ == '__main__':
    unittest.main()
