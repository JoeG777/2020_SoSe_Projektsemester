bereinigungs_config = {

    "sensor_data_timeframe": {
        "from": "2020-01-10 00:00:00.000 UTC",
        "to": "2020-01-13 12:00:00.000 UTC",
    },

    "sensor_data": {
        "from_db": "nilan",
        "to_db": "db_bereinigte_daten",
        "from_measurement": "temperature_register",
        "to_measurement": "temperature_register",
        "value_name": "valueScaled",
        "register": "201, 202, 204, 206, 205, 210",
        "frame_width": 100,
        "freq": "60S",
        "threshold": "3600S",
    },

    "historic_weatherdata": {
        "from_db": "db_rohdaten",
        "to_db": "db_bereinigte_daten",
        "from_measurement": "temperature_DWD",
        "to_measurement": "temperature_register",
        "value_name": "temperature",
        "register": "historic_weatherdata",
        "frame_width": 100,
        "freq": "60S",
        "threshold": "3600S",
    },

    "forecast_weatherdata": {
        "from_db": "db_rohdaten",
        "to_db": "db_bereinigte_daten",
        "from_measurement": "temperature_DWD",
        "to_measurement": "forecast_temperature_register",
        "value_name": "temperature",
        "register": "forecast_weatherdata",
        "frame_width": 100,
        "freq": "60S",
        "threshold": "10000S",
    }
}