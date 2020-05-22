import json
import unittest
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas
from mockito import mockito, ANY, captor, mock
from mockito.mockito import when2, when
import data_pipeline.log_writer.log_writer as logger

when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x, y: print(x))))
from data_pipeline.exception.exceptions import PersistorException, DBException, ConfigException
from data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine import training_engine as te
from prediction_core.model_persistor import model_persistor


class test_train(unittest.TestCase):
    def test_creates_model_with_valid_config(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "filtered_data",
                    "datasource_nilan_measurement": "temperature_register",
                    "datasource_weatherdata_dbname": "bereinigte_Daten",
                    "datasource_weatherdata_measurement": "temperature_register"
                },
                "prediction": {
                    "datasource_forecast_dbname": "bereinigte_Daten",
                    "datasource_forecast_measurement": "forecast_temperature_register",
                    "datasource_forecast_register": "201",
                    "datasink_prediction_dbname": "prediction_data",
                    "datasink_prediction_measurement": "vorhergesagteDaten"
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
        when2(rm.read_query, ANY(str), ANY(str)).thenReturn(pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "historic_weatherdata": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ), pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "freshAirIntake": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "inlet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "room": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "outlet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "evaporator": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "condenser": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ))
        when2(json.dumps, ANY).thenReturn("success!")
        model_captor = captor(ANY)
        when2(model_persistor.save, model_captor)

        te.train(valid_config)

        model = model_captor.value
        print(model)

    def test_valid_config_persistor_raises_exception(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "filtered_data",
                    "datasource_nilan_measurement": "temperature_register",
                    "datasource_weatherdata_dbname": "bereinigte_Daten",
                    "datasource_weatherdata_measurement": "temperature_register"
                },
                "prediction": {
                    "datasource_forecast_dbname": "bereinigte_Daten",
                    "datasource_forecast_measurement": "forecast_temperature_register",
                    "datasource_forecast_register": "201",
                    "datasink_prediction_dbname": "prediction_data",
                    "datasink_prediction_measurement": "vorhergesagteDaten"
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
        when2(rm.read_query, ANY(str), ANY(str)).thenReturn(pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "historic_weatherdata": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ), pandas.DataFrame(
            {
                "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "freshAirIntake": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "inlet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "room": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "outlet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "evaporator": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "condenser": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ))
        when2(model_persistor.save, ANY).thenRaise(PersistorException)

        self.assertRaises(PersistorException, te.train(valid_config))

    def test_valid_config_db_raises_exception(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "filtered_data",
                    "datasource_nilan_measurement": "temperature_register",
                    "datasource_weatherdata_dbname": "bereinigte_Daten",
                    "datasource_weatherdata_measurement": "temperature_register"
                },
                "prediction": {
                    "datasource_forecast_dbname": "bereinigte_Daten",
                    "datasource_forecast_measurement": "forecast_temperature_register",
                    "datasource_forecast_register": "201",
                    "datasink_prediction_dbname": "prediction_data",
                    "datasink_prediction_measurement": "vorhergesagteDaten"
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
        when2(rm.read_query, ANY(str), ANY(str)).thenRaise(DBException)

        with self.assertRaises(DBException):
            te.train(valid_config)

    def test_invalid_config_db_raises_exception(self):
        valid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "filtered_data",
                    "datasource_nilan_measurement": "temperature_register",
                    "datasource_weatherdata_dbname": "bereinigte_Daten",
                    "datasource_weatherdata_measurement": "temperature_register"
                },
                "prediction": {
                    "datasource_forecast_dbname": "bereinigte_Daten",
                    "datasource_forecast_measurement": "forecast_temperature_register",
                    "datasource_forecast_register": "201",
                    "datasink_prediction_dbname": "prediction_data",
                    "datasink_prediction_measurement": "vorhergesagteDaten"
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
                    }
                ]
            }
        }
        when2(rm.read_data, "weather_dbname", measurement="weather_measurement").thenRaise(DBException)

        with self.assertRaises(ConfigException):
            te.train(valid_config)


if __name__ == '__main__':
    unittest.main()
