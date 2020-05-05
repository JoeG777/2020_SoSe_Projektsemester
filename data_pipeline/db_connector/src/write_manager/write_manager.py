from data_pipeline.db_connector.src.db_config import db_config
from influxdb import InfluxDBClient
from datetime import datetime

url = db_config.params.get("url")
port = db_config.params.get("port")
user = db_config.params.get("user")
password = db_config.params.get("password")


def write_query(db, json):
    """
    Takes a parameter as JSON and writes the data defined in it into the influx database provided in db_config.
    :param db: The database the JSON should be written to.
    :param json: The json file to write into the database
    """
    client = InfluxDBClient(url, port, user, password, db)
    client.write_points(json)


def write_query_array(db, json_array):
    """
    Takes a parameter as JSON-Array and writes the data defined in it into the influx database provided in db_config.
    :param db: The database the JSON-Array should be written to.
    :param json_array: The JSON-Array to write into the database
    """
    client = InfluxDBClient(url, port, user, password, db)

    for json in json_array:
        client.write_points(json)


def write_value_with_time(db, measurement, value, value_name, time):
    """
    Takes a measurement, value, a value name and a time in utc, puts the value in a json format and writes them into the
    provided influx database.
    :param db: The database the JSON-Array should be written to.
    :param measurement: the name of the measurement to write as String.
    :param value: the value to write as String.
    :param value_name: the name of the value to write as String.
    :param time: the time to write in utc as String.
    """
    write_query(db, build_write_json(measurement, value, value_name, time))


def write_value_now(db, measurement, value, value_name):
    """
    Calls write_value_with_time with the current time.
    :param db: The database the value should be written to.
    :param measurement: the name of the measurement to write as String.
    :param value: the value to write as String.
    :param value_name: the name of the value to write as String.
    """
    write_value_with_time(db, measurement, value, value_name, datetime.utcnow())


def write_temperature_with_time(db, measurement, temperature, time):
    """
    Calls write_value_with_time with the the value_name variable set to "temperature".
    :param db: The database the temperature should be written to.
    :param measurement: the name of the measurement to write as String.
    :param temperature: the temperature value to write as String.
    :param time: the time to write in utc as String.
    """
    write_value_with_time(db, measurement, temperature, "temperature", time)


def build_write_json(measurement, value, value_name, time):
    """
    Takes a measurement, value, a value name and a time in utc and puts these variables into a json to be used with
    an influx client.
    :param measurement: the name of the measurement to write as String.
    :param value: the value to write as String.
    :param value_name: the name of the value to write as String.
    :param time: the time to write in utc as String.
    :return: the provided parameters in a json object.
    """
    json = [
        {'measurement': measurement,
         "time": int(time),
         "fields": {value_name: float(value)}
         }
    ]
    return json
