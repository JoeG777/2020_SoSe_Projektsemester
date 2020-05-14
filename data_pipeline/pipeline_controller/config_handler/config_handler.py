import requests

CONFIG_URL = "http://localhost:xxxx"
CONFIG_ENDPOINTS = {"elicitation": '/erhebung_config',
                    "cleaning": '/bereinigung_config',
                    "classification": '/klassifikation_config',
                    "filtering": '/filterung_config',
                    "prediction": '/vorhersage_config'
                    }


def fetch_all_configs():
    all_configs = {}
    for key in CONFIG_ENDPOINTS.keys():
        all_configs[key] = drop_get_request(CONFIG_URL + CONFIG_ENDPOINTS[key])
    return all_configs


def drop_get_request(url):
    return requests.get(url)