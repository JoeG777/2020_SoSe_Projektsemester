from influxdb import InfluxDBClient
from sklearn import linear_model
import pandas as pd
import numpy as np
import utils


def calculate_prediction(config_data):
    # TODO ADD OUTDOOR DATA RETRIEVAL HERE
    known_data_sources = {"outdoor": "check"}
    # TODO ADD MODEL RETRIEVAL
    all_prediction_models = {}
    while len(config_data) > 0:
        for prediction_unit in config_data:
            independent_data = prediction_unit.get("independent")
            dependent_data = prediction_unit.get("dependent")
            if utils.is_subset(independent_data, known_data_sources.keys()):
                config_data.remove(prediction_unit)
                apply_model(prediction_unit, known_data_sources, all_prediction_models)


def apply_model(prediction_unit, known_data_sources, all_prediction_models):
    independent_keys = prediction_unit.get("independent")
    dependent_keys = prediction_unit.get("dependent")
    model = get_model(prediction_unit)
    data_basis = []
    for key in known_data_sources.get_keys:
        if key in independent_keys:
            data_basis.append(known_data_sources.get(key))
    known_data_sources[dependent_keys] = model.predict(data_basis)


def get_model(prediction_unit):
    return ""

def classify(db_config):
    return ""

