vorhersage_config = {
    "database_options": {
        "training": {
            "datasource_nilan_dbname": "db_gefilterte_daten",
            "datasource_nilan_measurement": "temperature_register",
            "datasource_weatherdata_dbname": "db_bereinigte_daten",
            "datasource_weatherdata_measurement": "temperature_register"
        },
        "prediction": {
            "datasource_forecast_dbname": "db_bereinigte_daten",
            "datasource_forecast_measurement": "forecast_temperature_register",
            "datasource_forecast_register": "forecast_weatherdata",
            "datasink_prediction_dbname": "db_vorhersage_daten",
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