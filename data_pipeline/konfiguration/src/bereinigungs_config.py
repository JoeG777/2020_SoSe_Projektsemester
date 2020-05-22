bereinigungs_config = {

    "sensor_data": {
        "from_db": "nilan",
        "to_db": "bereinigte_Daten",
        "from_measurement": "temperature_register",
        "to_measurement": "temperature_register",
        "value_name": "valueScaled",
        "register": "201, 202, 204, 205, 206, 210",
        "frame_width": 100,
        "freq": "60S",
        "threshold": "3600S",
        "time": {
            "from": "1478610800000000000",
            "to": "1588292230546593792"
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
        "freq": "60S",
        "threshold": "3600S",
        "time": {
            "from": "1478610800000000000",
            "to": "1588292230546593792"
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
        "freq": "60S",
        "threshold": "10000S",
        "time": {
            "from": "1588292230546593792",
            "to": "1681375599000000000"
        }
    }

}
