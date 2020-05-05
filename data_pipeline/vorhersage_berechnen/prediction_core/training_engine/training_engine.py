import data_pipeline.db_connector.src.read_manager.read_manager as rm
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from data_pipeline.vorhersage_berechnen.prediction_core.model_persistor import model_persistor

default_measurement = "measurement"
nilan_db = "nilan"
temp_db = "darkSkyDaten"

register_dict = {
    "freshAirIntake": "201",
    "inlet": "202",
    "room": "210",
    "outlet": "204",
    "condenser": "205",
    "evaporator": "206"
}


def get_data(register):
    return rm.read_register_of_measurement(nilan_db, "temperature_register", register_dict[register])


def get_temperature():
    return rm.read_query_in_good(temp_db, "SELECT * FROM weatherTest LIMIT 50")


def get_all_data():
    keys = register_dict.keys()
    df = get_temperature()
    df = df.rename(columns={'temperature': "outdoor"})
    # -------
    # ONLY FOR TESTING!!!
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df = df.resample(rule='1S').bfill()
    # -------
    for key in keys:
        current_dataset = get_data(key)
        current_dataset = current_dataset.rename(columns={'valueScaled': key})
        # -------
        # ONLY FOR TESTING!!!
        current_dataset['time'] = pd.to_datetime(current_dataset['time'])
        current_dataset = current_dataset.set_index('time')
        current_dataset = current_dataset.resample(rule='1S').bfill()
        # -------
        df = pd.merge(df, current_dataset, on='time', how='inner')
    return df


def model_to_dict(score, model, dependent_data_keys):
    return {
        "dependent": dependent_data_keys,
        "score": float(score),
        "model": model
    }


def train_model(all_data, prediction_unit):
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

    return model_to_dict(model.score(independent_test, dependent_test), model, dependent_data_keys)


def calculate_average_score(all_models):
    score_sum = 0
    for model in all_models:
        score_sum += model["score"]
    return float(score_sum / len(all_models))


def save_prediction_model(all_models, config):
    avg_score = calculate_average_score(all_models)
    persist_dictionary = {
        "average_score": avg_score,
        "config": config,
        "models": all_models
    }
    model_persistor.save(persist_dictionary)


def train(config):
    all_models = []
    all_data = get_all_data()
    for prediction_unit in config:
        all_models.append(train_model(all_data, prediction_unit))
    save_prediction_model(all_models, config)


# ------------------------------ TESTONLY
default = [
    {
        "independent": ["freshAirIntake"],
        "dependent": ["condenser"],
        "test_sample_size": 0.2
    },
    {
        "independent": ["freshAirIntake"],
        "dependent": ["inlet"],
        "test_sample_size": 0.2
    },
    {
        "independent": ["freshAirIntake", "condenser", "evaporator"],
        "dependent": ["room"],
        "test_sample_size": 0.2
    },
    {
        "independent": ["freshAirIntake", "condenser"],
        "dependent": ["evaporator"],
        "test_sample_size": 0.2
    },
    {
        "independent": ["freshAirIntake"],
        "dependent": ["outlet"],
        "test_sample_size": 0.2
    }
]

train(default)
