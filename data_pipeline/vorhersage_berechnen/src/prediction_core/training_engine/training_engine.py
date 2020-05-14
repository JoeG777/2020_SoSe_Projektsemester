import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas as pd
import json
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor import model_persistor
from data_pipeline.vorhersage_berechnen.src.prediction_core.config_validator import config_validator
from data_pipeline.log_writer import log_writer as lw
from sklearn.metrics import explained_variance_score
from sklearn.metrics import max_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score


curves = ["freshAirIntake", "inlet", "room", "outlet", "condenser", "evaporator"]


def get_all_data(db_config):
    """
    Name in  documentation: TODO ADD TO DOCS
    Retrieves all data from the database defined in nilan_db and temp_db and merges this data into a dataframe.
    The dataframe then is returned.
    :return: A dataframe containing all data relevant for the model creation.
    """
    df = rm.read_data(db_config["datasource_weatherdata_dbname"], measurement=db_config["datasource_weatherdata_measurement"])
    df = df.rename(columns={'temperature': "outdoor"})
    current_dataset = rm.read_data(
        db_config["datasource_nilan_dbname"],
        measurement=db_config["datasource_nilan_measurement"],
        resolve_register="True")

    df = pd.merge(df, current_dataset, on='time', how='inner')

    return df


def build_unit_logging_model(models, current_model, indep_test, dep_true):
        model = current_model["model"]
        dep_predicted = model.predict(indep_test)
        current_model["explained_variance_score"] = explained_variance_score(dep_true, dep_predicted)
        current_model["max_error"] = max_error(dep_true, dep_predicted)
        current_model["mean_absolute_error"] = mean_absolute_error(dep_true, dep_predicted)
        current_model["mean_squared_error"] = mean_squared_error(dep_true, dep_predicted)
        current_model["median_absolute_error"] = median_absolute_error(dep_true, dep_predicted)
        current_model["r2_score"] = r2_score(dep_true, dep_predicted)
        models.append(current_model)


def build_and_write_logging_model(unit_logging_models, average_score):
    explained_variance_score_avg = 0
    max_error_avg = 0
    mean_absolute_error_avg = 0
    mean_squared_error = 0
    median_absolute_error_avg = 0
    r2_score_avg = 0
    print(unit_logging_models)
    logging_model_amount = len(unit_logging_models)
    for unit_logging_model in unit_logging_models:
        del(unit_logging_model["model"])
        explained_variance_score_avg += unit_logging_model["explained_variance_score"]
        max_error_avg += unit_logging_model["max_error"]
        mean_absolute_error_avg += unit_logging_model["mean_absolute_error"]
        mean_squared_error +=  unit_logging_model["mean_squared_error"]
        median_absolute_error_avg += unit_logging_model["median_absolute_error"]
        r2_score_avg += unit_logging_model["r2_score"]
    logging_model = {"average_score": average_score,
                     "average_explained_variance_score": explained_variance_score_avg/logging_model_amount,
                     "average_max_error": max_error_avg/logging_model_amount,
                     "average_mean_absolute_error": mean_absolute_error_avg/logging_model_amount,
                     "average_mean_squared_error": mean_squared_error/logging_model_amount,
                     "average_median_absolute_error": median_absolute_error_avg/logging_model_amount,
                     "average_r2_score_avg": r2_score_avg/logging_model_amount,
                     "model_scores": unit_logging_models
                     }
    logger = lw.Logger("Prediction Engine")
    print(logging_model)
    print(json.dumps(logging_model))
    logger.write_into_measurement("model", json.dumps(logging_model))


def model_data_to_dict(score, model, dependent_data_keys):
    """
    Name in  documentation: TODO ADD TO DOCS
    Takes a score, a model and the keys of the dependent data this model was created with and returns a dictionary.
    The structure of the dictionary is defined in 3.4.1.5.3 of the architecture documentation.
    :param score: The score this model reached.
    :param model: The model that should be persisted.
    :param dependent_data_keys: The keys for the dependent data the model was created with.
    :return: A dictionary containing all data as defined in 3.4.1.5.3
    """
    return {
        "dependent": dependent_data_keys,
        "score": float(score),
        "model": model
    }


def train_model(all_data, prediction_unit, log_models):
    """
    Name in  documentation: modell_trainieren
    Takes a list of dataframes and a prediction unit. Creates a model according to the prediction unit.
    :param all_data: A Dictionary of dataframes. Each independent curve of the prediction unit needs to be present here.
    :param prediction_unit: The prediction unit the model should be based on.
    :return: The created model in a dictionary as defined in model_data_to_dict.
    """
    model = linear_model.LinearRegression()

    independent_data_keys = prediction_unit["independent"]
    dependent_data_keys = prediction_unit["dependent"]
    test_sample_size = prediction_unit["test_sample_size"]

    independent_train, independent_test, dependent_train, dependent_test = train_test_split(
        all_data[independent_data_keys],
        all_data[dependent_data_keys],
        test_size=test_sample_size,
        random_state=0)
    model.fit(independent_train, dependent_train)
    score = model.score(independent_test, dependent_test)
    persistance_model = model_data_to_dict(score, model, dependent_data_keys)
    build_unit_logging_model(log_models, persistance_model, independent_test, dependent_test)
    return persistance_model


def calculate_average_score(all_models):
    """
    Name in  documentation: score_durchschnitt_berechnen
    Takes a list of models and calculates their average score.
    :param all_models: The list of models.
    :return: The average score.
    """
    score_sum = 0
    for model in all_models:
        score_sum += model["score"]
    print("Average Score: " + str(float(score_sum / len(all_models))))
    return float(score_sum / len(all_models))


def save_prediction_model(all_models, config):
    """
    Name in  documentation: vorhersagemodell_speichern()
    Takes a list of models and the corresponding configuration. Persists these as a dictionary as defined in 3.4.1.5.3.
    :param all_models: All models to be persisted.
    :param config: The config these models where created with.
    """
    avg_score = calculate_average_score(all_models)
    persist_dictionary = {
        "average_score": avg_score,
        "config": config,
        "models": all_models
    }
    model_persistor.save(persist_dictionary)
    return persist_dictionary


def train(config):
    """
    Name in  documentation: trainieren
    Takes a configuration and trains a regression model based on this configuration.
    :param config: The configuration the model should be created with.
    """
    print("------starting training--------------")
    config_validator.validate_config(config)
    all_models = []
    all_data = get_all_data(config["database_options"]["training"])
    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)
    log_models = []
    for prediction_unit in all_prediction_units:
        all_models.append(train_model(all_data, prediction_unit, log_models))
    persist_dictionary = save_prediction_model(all_models, config)
    build_and_write_logging_model(log_models, persist_dictionary["average_score"])
