import pandas as pd
from data_pipeline.log_writer import log_writer
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
from data_pipeline.daten_klassifizieren.config import classification_config as config
from datetime import datetime
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import time
import unittest
from data_pipeline.exception.exceptions import *


class test_enrich_data(unittest.TestCase):

    def test_return_invalidConfigKeyException(self):
        classification_config = {
            "selected_event": "abtauzyklus"
        }
        self.assertRaises(InvalidConfigKeyException, trainingsdata.enrich_data, classification_config)



    def test_return_invalidConfigValueException(self):
        classification_config = {
            "datasource_raw_data": {'database': 'test', 'measurement': 'temperature'},
            "datasource_enriched_data": {'database': 'nilan_enriched', 'measurement': 'training'},
            "datasource_marked_data": {'database': 'nilan_marked', 'measurement': 'training'},
            "timeframe": ["", "2020-01-20 12:0:00.000 UTC"],
            "selected_event": "abtauzyklus",
            "abtauzyklus": ['206', '205'],
            "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                              "206": "evaporator"},
            "event_features": {
                "start_marker": 1.0,
                "start_deriv": 1.7,
                "start_evap": 1.0,
                "start_ch": -0.06,
                "start_abtau": 10.0,
                "end_marker": -1.0,
                "end_deriv": 0.5,
                "end_deriv_n3": -0.65,
                "end_shift": -1.0,
                "del_marker": 0.0
            },
         }
        self.assertRaises(InvalidConfigValueException, trainingsdata.enrich_data, classification_config)

    def test_return_DBException(self):
        classification_config = {
            "datasource_raw_data": {'database': 'a', 'measurement': 'temperature'},
            "datasource_enriched_data": {'database': 'nilan_enriched', 'measurement': 'training'},
            "datasource_marked_data": {'database': 'nilan_marked', 'measurement': 'training'},
            "timeframe": ["2020-01-15 12:0:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
            "selected_event": "abtauzyklus",
            "abtauzyklus": ['206', '205'],
            "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                              "206": "evaporator"},
            "event_features": {
                "start_marker": 1.0,
                "start_deriv": 1.7,
                "start_evap": 1.0,
                "start_ch": -0.06,
                "start_abtau": 10.0,
                "end_marker": -1.0,
                "end_deriv": 0.5,
                "end_deriv_n3": -0.65,
                "end_shift": -1.0,
                "del_marker": 0.0
            }
        }
        self.assertRaises(DBException, trainingsdata.enrich_data, classification_config)
