from influxdb import InfluxDBClient
from sklearn import linear_model
import pandas as pd
import numpy as np
import data_pipeline.vorhersage_berechnen.prediction_core.config_validator.config_validator as cfg_validator
import data_pipeline.vorhersage_berechnen.prediction_core.model_persistor.model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as db_conn

OUTDOOR_REGISTER = '210'
MEASUREMENT = 'temperature_register'
DATABASE = 'nilan'


def calculate_prediction(config):
    cfg_validator.validate_config(config)

    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)

    known_data_sources = db_conn.read_register_of_measurement(DATABASE, MEASUREMENT, OUTDOOR_REGISTER)

    # TODO REMOVE
    print(known_data_sources.head())
    known_data_sources.columns = ['outdoor']
    # -------
    all_prediction_models = model_persistor.load()


    # TODO check if all_prediction_models are up to date

    while all_prediction_units:
        for prediction_unit in all_prediction_units:
            independent_data = prediction_unit.get("independent")
            if set(independent_data).issubset(set(known_data_sources.columns.values)):
                apply_model(prediction_unit, known_data_sources, all_prediction_models)
                all_prediction_units.remove(prediction_unit)

    # TODO write to database

    # TODO classify_prediciton


def apply_model(prediction_unit, known_data_sources, all_prediction_models):
    independent_keys = prediction_unit.get("independent")
    dependent_keys = prediction_unit.get("dependent")
    model = get_model(dependent_keys, all_prediction_models)

    independent_data = [known_data_sources[key] for key in independent_keys]

    predicted_data = model.predict(independent_data)

    # TODO include control params
    known_data_sources[dependent_keys] = predicted_data


def get_model(dependent_keys, all_prediction_models):
    models = all_prediction_models.get("models")

    for entry in models:
        dependent = entry.get("dependent")

        if dependent == dependent_keys:
            return entry.get("model")

    return None


def classify_prediction(db_config):
    return ""

