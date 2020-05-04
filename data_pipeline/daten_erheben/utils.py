from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from console_progressbar import ProgressBar


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
    client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'WetterDWD')
    client.create_database('WetterDWD')

    pb_forecast = ProgressBar(total=100, prefix='Daten schreiben', suffix='', decimals=2, length=50, fill='#', zfill='-')
    counter = 1

    for json in json_array:
        client.write_points(json)
        percent = float("{:.2f}".format((counter/len(json_array)*100)))
        counter += 1
        pb_forecast.print_progress_bar(percent)

    print("Daten aktualisiert.")