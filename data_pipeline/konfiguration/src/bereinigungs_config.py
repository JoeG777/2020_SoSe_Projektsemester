bereinigungs_config = {

    "sensor_data": {
        "from_db": "nilan",
        "to_db": "bereinigte_Daten",
        "from_measurement": "temperature_register",
        "to_measurement": "temperature_register",
        "value_name": "valueScaled",
        "register": "201, 202, 204, 206, 205, 210",
        "frame_width": 10,
        "freq": "60S",
        "threshold": 3600,
        "time": {
            "from": "1578610800000000000",
            "to": "1578913200000000000"
        }
    },

    "historic_weatherdata": {
        "from_db": "db_rohdaten",
        "to_db": "bereinigte_Daten",
        "from_measurement": "temperature_DWD",
        "to_measurement": "temperature_register",
        "value_name": "temperature",
        "register": "historic_weatherdata",
        "frame_width": 10,
        "freq": "600S",
        "threshold": 3600,
        "time": {
            "from": "1588809000000000000",
            "to": "1589413800000000000"
        }
    },

    "forecast_weatherdata": {
        "from_db": "db_rohdaten",
        "to_db": "bereinigte_Daten",
        "from_measurement": "temperature_DWD",
        "to_measurement": "forecast_temperature_register",
        "value_name": "temperature",
        "register": "forecast_weatherdata",
        "frame_width": 10,
        "freq": "3600S",
        "threshold": 10000,
        "time": {
            "from": "1588809000000000000",
            "to": "1589413800000000000"
        }
    }

}