from influxdb import InfluxDBClient
from sklearn import linear_model
import pandas as pd
import numpy as np
import data_pipeline.vorhersage_berechnen.prediction_core.config_validator.config_validator as cfg_validator
import data_pipeline.vorhersage_berechnen.prediction_core.model_persistor.model_persistor as model_persistor


def calculate_prediction(config):
    cfg_validator.validate_config(config)

    selected_option = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_option)

    # TODO ADD OUTDOOR DATA RETRIEVAL HERE
    known_data_sources = ['outdoor']

    all_prediction_models = model_persistor.load()

    # TODO check if all_prediction_models are up to date

    while all_prediction_units:
        for prediction_unit in all_prediction_units:
            independent_data = prediction_unit.get("independent")

            if set(independent_data).issubset(set(known_data_sources)):
                apply_model(prediction_unit, known_data_sources, all_prediction_models)
                config.remove(prediction_unit)


    # TODO classify_prediciton


def apply_model(prediction_unit, known_data_sources, all_prediction_models):
    independent_keys = prediction_unit.get("independent")
    dependent_keys = prediction_unit.get("dependent")
    model = get_model(all_prediction_models)

    # TODO extract all dependent curves out of known_data_sources (DATA FRAME)
    # TODO apply model
    # TODO add new predictions to known_data_sources



def get_model(all_prediction_models):
    # TODO extract model from all_prediction_models
    return ""

def classify_prediction(db_config):
    return ""

