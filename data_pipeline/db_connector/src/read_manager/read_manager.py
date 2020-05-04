from influxdb import InfluxDBClient
from ..db_config import db_config
import datetime

url = db_config.params.get("url")
port = db_config.params.get("port")
user = db_config.params.get("user")
password = db_config.params.get("password")
db = db_config.params.get("db_name")


def read_query(query):
    """
    Takes a query in the influx sql dialect. Sends this query to the client provided by the current config and returns
    the queries result.
    :param query: The query for the data retrieval.
    :return: The result of the query.
    """
    client = InfluxDBClient(url, port, user, password, db)
    data = client.query(query)
    points = list(data.get_points())
    result = []

    for p in points:
        result.append(p.get('valueScaled'))

    return result


def read_register_of_measurement(measurement, register):
    """
    Takes a measurement and a register, both as Strings, and returns the value present in these.
    :param measurement: The measurement the data should be retrieved from.
    :param register: The register the data should be retrieved from.
    :return: The retrieved data.
    """
    query = 'select * from ' + measurement + ' where register = \'' + register + '\''
    return read_query(query)


def read_register_of_measurement_from_to(measurement, register, start, end):
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
    return read_query(query)
