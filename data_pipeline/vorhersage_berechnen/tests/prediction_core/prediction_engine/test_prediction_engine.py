from unittest import TestCase

from mockito import *
from mockito.matchers import ANY, captor
from data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_engine.prediction_engine import *
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor.model_persistor as model_persistor
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_api.prediction_api
import pandas as pd
from sklearn import linear_model as lm, model_selection

# TODO prediction engine will change (send classification request and calc in control params,
#  tests need to be adjusted acordingly)


class test_calculate_prediction(TestCase):

    def test_config_is_valid_should_send_predictions_to_database(self):
        # valid config
        valid_config = {
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

        # all_prediction_models
        example_values = pd.DataFrame.from_dict({
            "time": [1.0, 2.0, 3.0],
            "outdoor": [1.0, 2.0, 3.0],
            "inlet": [2.0, 4.0, 6.0],  # outdoor * 2
            "room": [3.0, 6.0, 9.0],  # outdoor + inlet
            "freshAirIntake": [3.0, 3.0, 3.0],  # 3
            "condenser": [3.0, 3.0, 3.0],  # 3
            "evaporator": [3.0, 3.0, 3.0],  # 3
            "outlet": [3.0, 3.0, 3.0]  # 3
        })

        example_values["time"] = pd.to_datetime(example_values["time"])
        example_values = example_values.set_index("time")

        normal = lm.LinearRegression().fit(example_values[["outdoor"]], example_values[["inlet"]])
        multiple = lm.LinearRegression().fit(example_values[["inlet", "outdoor"]], example_values[["room"]])
        multivariate = lm.LinearRegression().fit(example_values[["room"]], example_values[["freshAirIntake", "condenser", "evaporator", "outlet"]])

        all_prediction_models = {
            "average_score": 0.91,
            "config": valid_config,
            "models": [
                {
                    "dependent": ["inlet"],
                    "model": normal,
                },
                {
                    "dependent": ["room"],
                    "model": multiple,
                },
                {
                    "dependent": ["freshAirIntake", "condenser", "evaporator", "outlet"],
                    "model": multivariate,
                },
            ]
        }

        # weather forecast
        temperature = {
            "time": [1, 2, 3],
            "valueScaled": [2, 4, 6]  # TODO might need to adjust the key of this
        }

        weather_forecast_dataframe = pd.DataFrame(temperature)

        # spies
        spy2(pred_api.send_classification_request)
        spy2(read_manager.read_data)
        spy2(write_manager.write_dataframe)

        # when the function tries to get the weather forecast from database, return the custom forecast DataFrame above
        when2(read_manager.read_data, ANY, measurement=ANY, register=ANY).thenReturn(weather_forecast_dataframe)

        # when the function tries to get the persisted models, pass the custom one from above
        when2(model_persistor.load).thenReturn(all_prediction_models)

        # when the function tries to write the prediction to the database, capture the prediction DataFrame
        forecast_captor = captor(any(pd.DataFrame))
        when2(write_manager.write_dataframe, forecast_captor, ANY, ANY)

        # call function under test with custom config above
        calculate_prediction(valid_config)

        # the actual prediction DataFrame
        actual_forecasts = forecast_captor.value

        expected_forecasts = pd.DataFrame.from_dict({
            "time": [1.0, 2.0, 3.0],
            "outdoor": [2.0, 4.0, 6.0],
            "inlet": [4.0, 8.0, 12.0],  # outdoor * 2
            "room": [6.0, 12.0, 18.0],  # outdoor + inlet
            "freshAirIntake": [3.0, 3.0, 3.0],  # 3
            "condenser": [3.0, 3.0, 3.0],  # 3
            "evaporator": [3.0, 3.0, 3.0],  # 3
            "outlet": [3.0, 3.0, 3.0],  # 3
        })

        # verify all interactions (default times is 1)
        verify(pred_api).send_classification_request(ANY)
        verify(read_manager).read_data(ANY, measurement=ANY, register=ANY)
        verify(write_manager).write_dataframe(ANY, ANY, ANY)

        pd.testing.assert_frame_equal(actual_forecasts, expected_forecasts, check_dtype=False)


