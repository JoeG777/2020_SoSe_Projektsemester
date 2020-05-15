import requests

from data_pipeline.pipeline_controller.request_service.request_service import drop_get_request

CONFIG_ENDPOINTS = {"elicitation": '/erhebung_config',
                    "cleaning": '/bereinigung_config',
                    "classification": '/klassifikation_config',
                    "filtering": '/filterung_config',
                    "prediction": '/vorhersage_config'
                    }


def fetch_all_configs():
    all_configs = {}
    for key in CONFIG_ENDPOINTS.keys():
        all_configs[key] = drop_get_request(CONFIG_ENDPOINTS[key])
    return all_configs


def fetch_config(config_key):
    return drop_get_request(CONFIG_ENDPOINTS[config_key])