from datetime import datetime
import pytz
import data_pipeline.db_connector.src.write_manager.write_manager as wm


def get_converted_date(date):
    '''
    This method sets the timezone of the timestamp to UTC in order to show it correctly in Grafana.
    :param date: Describes the Date you want to convert.
    :return: the date 2 hours before the passed date.
    '''

    timestamp = datetime(year = int(date[:4]), month = int(date[5:7]), day = int(date[8:10]), hour = int(date[11:13]), minute = int(date[14:16]), second = int(date[17:19]))
    local_timezone = pytz.timezone("Europe/Berlin")
    timezone = pytz.timezone("UTC")

    local_timestemp = local_timezone.localize(timestamp)
    timezone_timestamp = local_timestemp.astimezone(timezone)

    timestamp_formatted = str(timezone_timestamp)[:10] + "T" + str(timezone_timestamp)[11:19] + "Z"

    return timestamp_formatted


def write_to_influx(json_array):
    '''
    This Method transfer the data to the writemanager to write them in a database.
    :param json_array: The JSON-Array includes the data you want to write in the database.
    '''

    wm.write_query_array("db_rohdaten",json_array)

    print("Daten aktualisiert.")