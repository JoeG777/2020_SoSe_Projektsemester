import pandas as pd

from influxdb import InfluxDBClient
from ..db_config import db_config

url = db_config.params.get("url")
port = db_config.params.get("port")
user = db_config.params.get("user")
password = db_config.params.get("password")


def read_query_in_good(db, query):
    """
    Takes a query in the influx sql dialect. Sends this query to the client provided by the current config and returns
    the queries result. Calls format_data() on all retrieved sets.
    :param db: The database the query should be read from.
    :param query: The query for the data retrieval.
    :return: The result of the query.
    """
    client = InfluxDBClient(url, port, user, password, db)
    data = client.query(query)
    return pd.DataFrame(data.get_points())


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
    points = list(data.get_points())
    result = []
    for p in points:
        result.append(p.get('valueScaled'))

    return format_data(result)


def read_register_of_measurement(db, measurement, register):
    """
    Takes a measurement and a register, both as Strings, and returns the value present in these.
    :param db: The database the data should be read from.
    :param measurement: The measurement the data should be retrieved from.
    :param register: The register the data should be retrieved from.
    :return: The retrieved data.
    """
    query = 'select valueScaled from ' + measurement + ' where register = \'' + register + '\'' + ' LIMIT 50'
    return format_data(read_query_in_good(db, query))


def read_register_of_measurement_from_to(db, measurement, register, start, end):
    """
    Equal functionality as read_register_of_measurement, but does also take a start and an end time.
    Make sure to format time as "yyyy-mm-dd hh:mm:ss".
    :param measurement: The measurement the data should be retrieved from.
    :param register: The register the data should be retrieved from.
    :param start: The start date of the data set.
    :param end: The end date of the data set.
    :return: The retrieved data.
    """
    query = 'select * from ' + measurement \
            + 'where time > \'' + start \
            + '\' and time < \'' + end \
            + '\' and register = \'' + register + '\''
    return format_data(read_query(db, query))


def format_data(dataset):
    """
    Formats a given dataset into a pandas DataFrame.
    :param dataset: The dataset to format.
    :return: The given dataset as a DataFrame.
    """
    return pd.DataFrame(dataset)
