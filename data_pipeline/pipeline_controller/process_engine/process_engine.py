import requests
import json

DATA_ELICITATION_URL = "http://localhost:xxxx"
DATA_CLEANING_URL = "http://localhost:xxxx"
DATA_CLASSIFICATION_URL = "http://localhost:xxxx"
DATA_FILTER_URL = "http://localhost:xxxx"
DATA_PREDICTION_URL = "http://localhost:4999"
CONFIG_URL = "http://localhost:xxxx"
CONFIG_ENDPOINTS = {"elicitation": '/erhebung_config',
                    "cleaning": '/bereinigung_config',
                    "classification": '/klassifikation_config',
                    "filtering": '/filterung_config',
                    "prediction": '/vorhersage_config'
                    }


def drop_get_request(url):
    return requests.get(url)


def drop_post_request(url, payload):
    return requests.post(url, json=json.dumps(payload))


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


def fetch_all_configs():
    all_configs = {}
    for key in CONFIG_ENDPOINTS.keys():
        all_configs[key] = drop_get_request(CONFIG_URL + CONFIG_ENDPOINTS[key])
    return all_configs


def start_timer_based_process_cycle():
    all_configs = fetch_all_configs()
    start_historic_data_elicitation(all_configs["elicitation"])
    start_prediction_data_elicitation(all_configs["elicitation"])
    start_cleaning(all_configs["cleaning"])
    start_classification(all_configs["classification"])
    start_classification_training(all_configs["classification"])
    start_filtering(all_configs["filtering"])
    start_prediction_training(all_configs["prediction"])


def start_trigger_based_process():
    config = drop_get_request(CONFIG_URL + "/vorhersage_config")
    start_prediction(config)

config = {
    "database_options": {
        "training": {
            "datasource_nilan_dbname": "trainingsdatenTest",
            "datasource_nilan_measurement": "trainingsdatenTestMeasurement",
            "datasource_weatherdata_dbname": "trainingsdatenTest",
            "datasource_weatherdata_measurement": "trainingswetterdatenTestMeasurement"
        },
        "prediction": {
            "datasource_forecast_dbname": "vorhersagedatenTest",
            "datasource_forecast_measurement": "vorhersageTestMeasurement",
            "datasource_forecast_register": "201",
            "datasink_prediction_dbname": "jourfixeVorhersage",
            "datasink_prediction_measurement": "vorhergesagteDaten"
        }
    },
    "selected_value": "default",
    "prediction_options": {
        "default": [
            {
                "independent": [
                    "outdoor"
                ],
                "dependent": [
                    "freshAirIntake"
                ],
                "test_sample_size": 0.2
            },
            {
                "independent": [
                    "freshAirIntake"
                ],
                "dependent": [
                    "evaporator"
                ],
                "test_sample_size": 0.2
            },
            {
                "independent": [
                    "freshAirIntake"
                ],
                "dependent": [
                    "outlet"
                ],
                "test_sample_size": 0.2
            },
            {
                "independent": [
                    "outlet",
                    "evaporator"
                ],
                "dependent": [
                    "room"
                ],
                "test_sample_size": 0.2
            },
            {
                "independent": [
                    "outdoor",
                    "freshAirIntake"
                ],
                "dependent": [
                    "inlet"
                ],
                "test_sample_size": 0.2
            },
            {
                "independent": [
                    "outdoor",
                    "freshAirIntake"
                ],
                "dependent": [
                    "condenser"
                ],
                "test_sample_size": 0.2
            }
        ]
    }
}

start_prediction_training(config)
