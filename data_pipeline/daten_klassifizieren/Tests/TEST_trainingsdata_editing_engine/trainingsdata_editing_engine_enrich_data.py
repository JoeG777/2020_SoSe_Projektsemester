import pandas as pd
from data_pipeline.log_writer import log_writer
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
from data_pipeline.daten_klassifizieren.config import classification_config as config
from datetime import datetime
from data_pipeline.daten_klassifizieren.config import classification_config as config
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import time
import unittest
from data_pipeline.exception.exceptions import *


class test_enrich_data(unittest.TestCase):

    def test_key_missing_in_config(self):
        wrong_config = config.copy()
        wrong_config.pop("selected_event")
        self.assertRaises(InvalidConfigKeyException, trainingsdata.enrich_data, wrong_config)

    def test_value_missing_in_config(self):
        wrong_config = config.copy()
        wrong_config['timeframe'][0] = ""
        self.assertRaises(InvalidConfigValueException, trainingsdata.enrich_data, wrong_config)



