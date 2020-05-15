import requests
import json

DATA_ELICITATION_URL = "http://localhost:4994"
DATA_CLEANING_URL = "http://localhost:4995"
DATA_CLASSIFICATION_URL = "http://localhost:4996"
DATA_FILTER_URL = "http://localhost:4997"
DATA_PREDICTION_URL = "http://localhost:4999"
CONFIG_URL = "http://localhost:4998"


def drop_get_request(url):
    return requests.get(url)


def drop_post_request(url, payload):
    return requests.post(url, json=json.dumps(payload))


def retrieve_config(config_endpoint):
    return drop_get_request(CONFIG_URL + config_endpoint)


def start_historic_data_elicitation(config):
    return drop_post_request(DATA_ELICITATION_URL + "/historische_daten_erheben ", config)


def start_prediction_data_elicitation(config):
    return drop_post_request(DATA_ELICITATION_URL + "/vorhersagedaten_erheben ", config)


def start_cleaning(config):
    return drop_post_request(DATA_CLEANING_URL + "/datenbereinigung", config)


def start_classification(config):
    return drop_post_request(DATA_CLASSIFICATION_URL + "/classify", config)


def start_classification_training(config):
    return drop_post_request(DATA_CLASSIFICATION_URL + "/train", config)


def start_filtering(config):
    return drop_post_request(DATA_PREDICTION_URL + "/filtern", config)


def start_prediction_training(config):
    return drop_post_request(DATA_PREDICTION_URL + "/train", config)


def start_prediction(config):
    return requests.post(DATA_PREDICTION_URL + "/predict", config)