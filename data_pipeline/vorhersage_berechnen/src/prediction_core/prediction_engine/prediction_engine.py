import pandas as pd
import data_pipeline.vorhersage_berechnen.src.prediction_core.config_validator.config_validator as cfg_validator
import data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor.model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as db_read
import data_pipeline.db_connector.src.write_manager.write_manager as db_write

OUTDOOR_REGISTER = "210"
FILTER_MEASUREMENT = "temperature_register"
FILTER_DATABASE_NAME = "nilan"
PREDICTION_DATABASE_NAME = "nilan"
PREDICTION_MEASUREMENT = "temperature_register"


def calculate_prediction(config):
    cfg_validator.validate_config(config)

    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)

    known_data_sources = db_read.read_data(
        FILTER_DATABASE_NAME, measurement=FILTER_MEASUREMENT, register=OUTDOOR_REGISTER)

    known_data_sources = known_data_sources.rename(columns={'valueScaled': 'outdoor'})

    all_prediction_models = model_persistor.load()

    while all_prediction_units:
        for prediction_unit in all_prediction_units:
            independent_data = prediction_unit.get("independent")
            if set(independent_data).issubset(set(known_data_sources.columns.values)):
                apply_model(prediction_unit, known_data_sources, all_prediction_models)
                all_prediction_units.remove(prediction_unit)

    db_write.write_dataframe(known_data_sources, PREDICTION_DATABASE_NAME, PREDICTION_MEASUREMENT)

    # TODO classify prediction


def apply_model(prediction_unit, known_data_sources, all_prediction_models):
    # TODO add control params from UI Engine
    independent_keys = prediction_unit.get("independent")
    dependent_keys = prediction_unit.get("dependent")
    model = get_model(dependent_keys, all_prediction_models)

    independent_data = known_data_sources[independent_keys]
    predicted_data = model.predict(independent_data)

    count = 0
    # loop is needed because predicted data can have multiple values in multivariate regression
    for key in dependent_keys:
        known_data_sources[key] = predicted_data[:, count]
        count += 1


def get_model(dependent_keys, all_prediction_models):
    models = all_prediction_models.get("models")

    for entry in models:
        dependent = entry.get("dependent")

        if dependent == dependent_keys:
            return entry.get("model")

    return None


def classify_prediction(db_config):
    a = 1
    #TODO classify prediction

