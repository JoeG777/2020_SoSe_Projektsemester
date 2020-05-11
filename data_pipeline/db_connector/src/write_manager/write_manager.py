import calendar
import time

from data_pipeline.db_connector.src.db_config import db_config
from influxdb import InfluxDBClient
from influxdb import DataFrameClient

url = db_config.params.get("url")
port = db_config.params.get("port")
user = db_config.params.get("user")
password = db_config.params.get("password")

default_measurement = "temperature"
default_value_name = "valueScaled"

batch_size = 1000
default_protocol = "line"
numeric_precision = "full"


def write_query(db, json):
    """
    Takes a parameter as JSON and writes the data defined in it into the influx database provided in db_config.
    :param db: The database the JSON should be written to.
    :param json: The json file to write into the database
    """
    InfluxDBClient(url, port, user, password, db).write_points(json)


def write_query_array(db, json_array):
    """
    Takes a parameter as JSON-Array and writes the data defined in it into the influx database provided in db_config.
    :param db: The database the JSON-Array should be written to.
    :param json_array: The JSON-Array to write into the database
    """
    client = InfluxDBClient(url, port, user, password, db)

    for json in json_array:
        client.write_points(json)


def write_single_value(db, value, **kwargs):
    """
    Takes a measurement, value, a value name and a time in utc, puts the value in a json format and writes them into the
    provided influx database.
    To define a custom measurement, add 'measurement = "my_measurement"'.
    To define a custom value name, add 'value_name = "my_value_name"'.
    To define a custom time, add 'time_utc = my_time'. Note that the time should be provided in utc.
    :param db: The database the JSON-Array should be written to.
    :param value: the value to write as String.
    """
    measurement = default_measurement
    if "measurement" in kwargs.keys():
        measurement = kwargs["measurement"]
    value_name = default_value_name
    if "value_name" in kwargs.keys():
        value_name = kwargs["value_name"]
    time = datetime.utcnow()
    if "time_utc" in kwargs.keys():
        time = kwargs["time_utc"]
    write_query(db, build_write_json(measurement, value, value_name, time))


def write_multiple_values(db, values, **kwargs):
    """
    Takes a list of measurements, a list of value, a list of value names and a list of time values in utc.
    Calls write_single_value with each value set.
    To define a custom measurement, add 'measurements = ["my_measurement1", "my_measurement2", ...]'.
    To define a custom value name, add 'value_names = ["my_value_name1", "my_value_name2"...]'.
    To define a custom time, add 'time_utc = [my_time1, my_time2,...]'. Note that the time should be provided in utc.
    :param db: The database the JSON-Array should be written to.
    :param values: the value to write as String.
    """
    for argument in kwargs:
        if len(kwargs[argument]) != len(values):
            raise ValueError("Argument length should be equal but was "
                             + str(len(kwargs[argument]))
                             + " and "
                             + str(len(values))
                             )
    index = 0
    for value in values:
        measurement = default_measurement
        if "measurement" in kwargs.keys():
            measurement = kwargs["measurement"][index]
        value_name = default_value_name
        if "value_name" in kwargs.keys():
            value_name = kwargs["value_name"][index]
        time = datetime.utcnow()
        if "time_utc" in kwargs.keys():
            time = kwargs["time_utc"][index]
        write_single_value(db, value, value_name=value_name, measurement=measurement, time=time)


def write_dataframe(db, dataframe, measurement):
    """
    Writes a given dataframe in a given measurement in a given database
    :param db: The database name as String
    :param dataframe: The dataframe to write.
    :param measurement: The measurement name as String
    :return:
    """
    DataFrameClient(url, port, user, password, db).write_points(
        batch_size=batch_size,
        dataframe=dataframe,
        protocol=default_protocol,
        measurement=measurement
    )


def build_write_json(measurement, value, value_name, time_value):
    """
    Takes a measurement, value, a value name and a time in utc and puts these variables into a json to be used with
    an influx client.
    :param measurement: the name of the measurement to write as String.
    :param value: the value to write as String.
    :param value_name: the name of the value to write as String.
    :param time_value: the time to write in utc as String.
    :return: the provided parameters in a json object.
    """
    json = {
        'measurement': measurement,
        "time": int(time_value),
        "fields": {value_name: float(value)}
    }

    return json
