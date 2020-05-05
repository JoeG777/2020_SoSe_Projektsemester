<<<<<<<< HEAD:data_pipeline/vorhersage_berechnen/src/prediction_core/training_engine/training_engine.py
import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor import model_persistor
========
>>>>>>>> Refactored file structure + made train recieve the full config.:data_pipeline/vorhersage_berechnen/prediction_core/training_engine/training_engine.py


def train(config):
    all_models = []
    for prediction_unit in config:
        all_models.append(train_model(prediction_unit))
        get_data()

def save_prediction_model(all_models, config):
    return ""


<<<<<<<< HEAD:data_pipeline/vorhersage_berechnen/src/prediction_core/training_engine/training_engine.py
def train(config):
    all_models = []
    all_data = get_all_data()
    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)
    for prediction_unit in all_prediction_units:
        all_models.append(train_model(all_data, prediction_unit))
    save_prediction_model(all_models, config)
========
def train_model(prediction_unit):
    return ""

>>>>>>>> Refactored file structure + made train recieve the full config.:data_pipeline/vorhersage_berechnen/prediction_core/training_engine/training_engine.py

def get_data():


def calculate_average_score():
    return""