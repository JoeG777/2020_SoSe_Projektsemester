from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from console_progressbar import ProgressBar
import data_pipeline.db_connector.src.write_manager.write_manager as wm


def get_converted_date(date):
    '''
    Diese Methode zieht von dem übergebenen Datum 2 Stunden ab damit es in Grafana richtig angezeigt werden kann.
    '''
    last_time = datetime(year = int(date[:4]), month = int(date[5:7]), day = int(date[8:10]), hour = int(date[11:13]), minute = int(date[14:16]), second = int(date[17:19]))
    two_hours = timedelta(hours = 2)

    time = str(last_time - two_hours)
    time_split = time.split(" ")

    return_time = time_split[0] + "T" + time_split[1] + "Z"

    return return_time


def write_to_influx(json_array):
    '''
    Diese Methode erstellt die WetterDWD Datenbank, baut eine Verbindung zu dieser auf und schreibt Daten aus einem
    übergebenen JSON-Array in die Datenbank. Bei Erfolgreichem schreiben kommt am Ende die Nachricht Daten aktualisiert.
    '''

    wm.write_query_array(json_array)

    print("Daten aktualisiert.")