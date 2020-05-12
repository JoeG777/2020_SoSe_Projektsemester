import unittest
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas

from mockito import mockito, ANY, captor
from mockito.mockito import when2
from data_pipeline.exception.exceptions import PersistorException, DBException
from data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine import training_engine as te

#TODO EXCEPTION BEI DBCONNECTOR
#TODO FEHLER BEIM PERSISTIEREN
from prediction_core.model_persistor import model_persistor


class test_train(unittest.TestCase):
    def test_creates_model_with_valid_config(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "nilan_db",
                    "datasource_nilan_measurement": "nilan_measurement",
                    "datasource_weatherdata_dbname": "weather_dbname",
                    "datasource_weatherdata_measurement": "weather_measurement",
                }
            },
            "selected_value": "default",
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["inlet"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["inlet", "outdoor"],
                        "dependent": ["room"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["room"],
                        "dependent": ["freshAirIntake", "condenser", "evaporator", "outlet"],
                        "test_sample_size": 0.2
                    }
                ]
            }
        }
        when2(rm.read_data, "nilan_db", measurement="nilan_measurement", register=ANY(str),
              resolve_register="True").thenReturn(pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "valueScaled": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ))
        when2(rm.read_data, "weather_dbname", measurement="weather_measurement").thenReturn(
            pandas.DataFrame(
                {
                    "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "temperature": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                }
            )
        )
        model_captor = captor(ANY)
        when2(model_persistor.save, model_captor)

        te.train(valid_config)

        model = model_captor.value
        print(model)

    def test_valid_config_persistor_raises_exception(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "nilan_db",
                    "datasource_nilan_measurement": "nilan_measurement",
                    "datasource_weatherdata_dbname": "weather_dbname",
                    "datasource_weatherdata_measurement": "weather_measurement",
                }
            },
            "selected_value": "default",
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["inlet"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["inlet", "outdoor"],
                        "dependent": ["room"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["room"],
                        "dependent": ["freshAirIntake", "condenser", "evaporator", "outlet"],
                        "test_sample_size": 0.2
                    }
                ]
            }
        }
        when2(rm.read_data, "nilan_db", measurement="nilan_measurement", register=ANY(str),
              resolve_register="True").thenReturn(pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "valueScaled": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ))
        when2(rm.read_data, "weather_dbname", measurement="weather_measurement").thenReturn(
            pandas.DataFrame(
                {
                    "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "temperature": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                }
            )
        )
        when2(model_persistor.save, ANY).thenRaise(PersistorException)

        self.assertRaises(PersistorException, te.train(valid_config))

    def test_valid_config_db_raises_exception(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "nilan_db",
                    "datasource_nilan_measurement": "nilan_measurement",
                    "datasource_weatherdata_dbname": "weather_dbname",
                    "datasource_weatherdata_measurement": "weather_measurement",
                }
            },
            "selected_value": "default",
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["inlet"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["inlet", "outdoor"],
                        "dependent": ["room"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["room"],
                        "dependent": ["freshAirIntake", "condenser", "evaporator", "outlet"],
                        "test_sample_size": 0.2
                    }
                ]
            }
        }
        when2(rm.read_data, "weather_dbname", measurement="weather_measurement").thenRaise(DBException)

        with self.assertRaises(DBException):
            te.train(valid_config)


if __name__ == '__main__':
    unittest.main()
