import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_engine.prediction_engine as pe
import data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine.training_engine as te
import data_pipeline.db_connector.src.read_manager.read_manager as db_conn
import data_pipeline.vorhersage_berechnen.src.prediction_core.model_persistor.model_persistor as mp
from sklearn import linear_model as lm
import pandas as pd

params = {
    "selected_value" : "default",
    "prediction_options" : {
        "default": [
            {
                "independent": ["outdoor"],
                "dependent": ["freshAirIntake"],
                "test_sample_size": 0.2
            },
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
                "independent": ["freshAirIntake", "condenser"],
                "dependent": ["room"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["condenser"],
                "dependent": ["evaporator", "outlet"],
                "test_sample_size": 0.2
            },
        ]
    },
}


one = db_conn.read_data('nilan', register='freshAirIntake', measurement='temperature_register')
two = db_conn.read_data('nilan', register='freshAirIntake', measurement='temperature_register')
four = db_conn.read_data('nilan', register='freshAirIntake', measurement='temperature_register')

one = one.rename(columns={'valueScaled': 'freshAirIntake'})
one = one.resample(rule='1S').bfill()

four = four.rename(columns={'valueScaled': 'inlet'})
four = four.resample(rule='1S').bfill()

normal = lm.LinearRegression().fit(one, four)
one = one.merge(four, on='time')

two = two.rename(columns={'valueScaled': 'condenser'})
two = two.resample(rule='1S').bfill()

multivariate = lm.LinearRegression().fit(two, one)

print(one.head())
print(two.head())


multiple = lm.LinearRegression().fit(one, two)


persisted = {
    "average_score": 0.91,
    "config": params,
    "models": [
        {
            "dependent": ["freshAirIntake"],
            "model": normal,
        },
        {
            "dependent": ["condenser"],
            "model": normal,
        },
        {
            "dependent": ["inlet"],
            "model": normal,
        },
        {
            "dependent": ["room"],
            "model": multiple
        },
        {
            "dependent": ["evaporator", "outlet"],
            "model": multivariate
        },
    ]
}


pe.calculate_prediction(params)

'''
params = {
    "selected_value" : "default",
    "prediction_options" : {
        "default": [
            {
                "independent": ["outdoor"],
                "dependent": ["inlet"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["inlet", "outdoor"],
                "dependent": ["room"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["room"],
                "dependent": ["freshAirIntake", "condenser", "evaporator", "outlet"],
                "test_sample_size": 0.2
            }
        ]
    }
}

te.train(params)

pe.calculate_prediction(params)

temperature = {
    "time": [1,2,3],
    "outdoor": [1,2,3],
    "inlet": [2,4,6],
    "room": [3,6,9],
    "freshAirIntake": [2,4,6],
    "yalla": [1,2,3],
}
'''