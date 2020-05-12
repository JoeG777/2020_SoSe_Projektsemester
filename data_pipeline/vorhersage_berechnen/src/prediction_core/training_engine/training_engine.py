import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor import model_persistor
from data_pipeline.vorhersage_berechnen.src.prediction_core.config_validator import config_validator

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

    for key in curves:
        current_dataset = rm.read_data(
            db_config["datasource_nilan_dbname"],
            measurement=db_config["datasource_nilan_measurement"],
            register=key,
            resolve_register="True")
        current_dataset = current_dataset.rename(columns={'valueScaled': key})

        df = pd.merge(df, current_dataset, on='time', how='inner')

    return df


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


def train_model(all_data, prediction_unit):
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

    return model_data_to_dict(score, model, dependent_data_keys)


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


def train(config):
    """
    Name in  documentation: trainieren
    Takes a configuration and trains a regression model based on this configuration.
    :param config: The configuration the model should be created with.
    """
    config_validator.validate_config(config)
    all_models = []
    all_data = get_all_data(config["database_options"]["training"])
    selected_value = config.get("selected_value")
    all_prediction_units = config.get("prediction_options").get(selected_value)
    for prediction_unit in all_prediction_units:
        all_models.append(train_model(all_data, prediction_unit))
    save_prediction_model(all_models, config)