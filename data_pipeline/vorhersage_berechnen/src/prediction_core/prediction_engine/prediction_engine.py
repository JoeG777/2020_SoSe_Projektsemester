import pandas as pd
import data_pipeline.vorhersage_berechnen.src.prediction_core.config_validator.config_validator as cfg_validator
import data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor.model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as db_read
import data_pipeline.db_connector.src.write_manager.write_manager as db_write
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_api.prediction_api as pred_api
import requests
from data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_api.prediction_api import logger

FETCH_CONFIG_URL = "http://localhost:5000/config"
PREDICTION_CLASSIFIED = "prediction_classified"


def calculate_prediction(config):
    logger.info("Starting prediction calculation...")
    cfg_validator.validate_config(config)

    database_options = config["database_options"]["prediction"]
    datasource_forecast_dbname = database_options.get("datasource_forecast_dbname")
    datasource_forecast_measurement = database_options.get("datasource_forecast_measurement")
    datasource_forecast_register = database_options.get("datasource_forecast_register")
    datasink_prediction_dbname = database_options.get("datasink_prediction_dbname")
    datasink_prediction_measurement = database_options.get("datasink_prediction_measurement")

    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)
    known_data_sources = db_read.read_data(datasource_forecast_dbname, measurement=datasource_forecast_measurement)
    known_data_sources = known_data_sources.astype('float64')
    known_data_sources = known_data_sources.rename(columns={datasource_forecast_register: 'outdoor'})
    time_start = known_data_sources.first_valid_index()
    time_end = known_data_sources.last_valid_index()
    logger.info("Fetched relevant data...")

    all_prediction_models = model_persistor.load()
    while all_prediction_units:
        logger.info("Known data sources: " + ', '.join(known_data_sources.columns.values))
        for prediction_unit in all_prediction_units:
            independent_data = prediction_unit.get("independent")
            if set(independent_data).issubset(set(known_data_sources.columns.values)):
                logger.info("Predicting " + ', '.join(prediction_unit.get("dependent")))
                apply_model(prediction_unit, known_data_sources, all_prediction_models)
                all_prediction_units.remove(prediction_unit)

    logger.info("Prediction finished. Sending data to database")
    db_write.write_dataframe(datasink_prediction_dbname, known_data_sources, datasink_prediction_measurement)
    classify_prediction(time_start, time_end, config)


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


def fetch_classification_data():
    payload = {"config": "classification"}
    return requests.post(FETCH_CONFIG_URL, json=payload)


def classify_prediction(start, end, config):
    classifiction_config = fetch_classification_data().json()
    datasource_raw_data = {
        "database": config["database_options"]["prediction"]["datasink_prediction_dbname"],
        "measurement": config["database_options"]["prediction"]["datasink_prediction_measurement"]
    }
    datasource_classified_data = {
        "database": config["database_options"]["prediction"]["datasink_prediction_dbname"],
        "measurement": PREDICTION_CLASSIFIED
    }

    classifiction_config["datasource_raw_data"] = datasource_raw_data
    classifiction_config["datasource_classified_data"] = datasource_classified_data
    # classifiction_config["timeframe"] = [str(start) + " UTC", str(end) + " UTC"]

    start = str(start)[:18] + ".000 UTC"
    end = str(end)[:18] + ".000 UTC"
    classifiction_config["timeframe"] = [start, end]
    classifiction_config['selected_event'] = "pred"
    pred_api.send_classification_request(classifiction_config)
