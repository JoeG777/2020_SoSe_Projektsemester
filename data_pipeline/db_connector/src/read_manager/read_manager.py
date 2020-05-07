import pandas as pd

from influxdb import InfluxDBClient
from ..db_config import db_config

default_measurement = "temperature"
default_register = "201"

url = db_config.params.get("url")
port = db_config.params.get("port")
user = db_config.params.get("user")
password = db_config.params.get("password")

register_dict = {
    "freshAirIntake": "201",
    "inlet": "202",
    "room": "210",
    "outlet": "204",
    "condenser": "205",
    "evaporator": "206"
}


def read_query(db, query):
    """
    Takes a query in the influx sql dialect. Sends this query to the client provided by the current config and returns
    the queries result. Calls format_data() on all retrieved sets.
    :param db: The database the query should be read from.
    :param query: The query for the data retrieval.
    :return: The result of the query.
    """
    client = InfluxDBClient(url, port, user, password, db)
    data = client.query(query)
    return format_data(data.get_points())


def read_data(db, **kwargs):
    """
    Takes a String that resembles the database the influx client should connect to. Further takes these
    optional arguments (note that ALL arguments need to be provided as Strings):
    measurement: define a specific measurement the data should be retrived from.
    register: The number of the register the data should be read from.
    resolve_register: If this variable is set, you can just use the curves names as defined in the register_dict.
                      The register names are mapped to the respective numbers.
    start_utc: The start date and time formatted in utc.
    end_utc: The start date and time formatted in utc.
    :param db: The database the data should be read from.
    :return: The retrieved data.
    """
    measurement = default_measurement
    if kwargs["measurement"]:
        measurement = kwargs["measurement"]
    register = default_register
    query = 'select * from ' + measurement
    if kwargs["register"]:
        if kwargs["resolve_register"]:
            register = register_dict[register]
        else:
            register = kwargs["register"]
        query += ' where register = \'' + register + '\''
    if kwargs["start_utc"]:
        if kwargs["register"]:
            query += ' AND '
        else:
            query += ' WHERE '
        query += 'AND time >' + kwargs["start"]
    if kwargs["end_utc"]:
        if kwargs["register"] | kwargs["end_utc"]:
            query += ' AND '
        else:
            query += ' WHERE '
        query += 'AND time <' + kwargs["end"]
    return read_query(db, query)


def format_data(dataset):
    """
    Formats a given dataset into a pandas DataFrame.
    :param dataset: The dataset to format.
    :return: The given dataset as a DataFrame.
    """
    df = pd.DataFrame(dataset)
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    return df
