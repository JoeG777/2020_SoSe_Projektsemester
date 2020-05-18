from unittest import TestCase
from mockito import when, when2, ANY, patch, mock
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))
import json
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_api.prediction_api as pred_api
import data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine.training_engine as te

class test_train(TestCase):

    def test_invalid_config_should_return_400(self):
        cfg = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
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

        self.app = pred_api.app.test_client()
        when2(te.train, ANY).thenReturn("YOLO")
        response = self.app.post('/train', data=json.dumps(cfg))
        assert '400' in str(response.status_code)
