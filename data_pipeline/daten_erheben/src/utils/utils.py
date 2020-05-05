from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from console_progressbar import ProgressBar
import data_pipeline.db_connector.src.write_manager.write_manager as wm


def get_converted_date(date):
    '''
    This method removes 2 hours from the passed date in order to show it correctly in Grafana.
    :param date: Describes the Date you want to convert.
    :return: the date 2 hours before the passed date.
    '''
    last_time = datetime(year = int(date[:4]), month = int(date[5:7]), day = int(date[8:10]), hour = int(date[11:13]), minute = int(date[14:16]), second = int(date[17:19]))
    two_hours = timedelta(hours = 2)

    time = str(last_time - two_hours)
    time_split = time.split(" ")

    return_time = time_split[0] + "T" + time_split[1] + "Z"

    return return_time


def write_to_influx(json_array):
    '''
    This Method transfer the data to the writemanager to write them in a database.
    :param json_array: The JSON-Array includes the data you want to write in the database.
    '''

    wm.write_query_array(json_array)

    print("Daten aktualisiert.")