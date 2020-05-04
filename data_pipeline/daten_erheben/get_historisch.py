from zipfile import ZipFile
import os
import requests
from io import BytesIO
import pandas as pd
import data_pipeline.daten_erheben.utils as utils
from data_pipeline.daten_erheben.exception import file_exception, url_exception, raw_data_exception
import data_pipeline.daten_erheben.log_writer as logger

dateTmpFile = "/tmp/tmp.txt"

"""
Formatiert den Zeitstempel der einzelnen Wetterdaten in ein geeignetes Format für das Einschreiben in InfluxDB.
"""
def get_timestamp_dwd(time):

    formatted = time[:4] + "-" + time[4:6] + "-" + time[6:8] + "T" + time[8:10] + ":" + time[10:12] + ":00Z"
    return formatted

""""
Das Start- und das Enddatum der anzufragenden Wetterdaten wird bestimmt und zurückgegeben. 
Für das bestimmen des Startdatums wird nach einem Eintrag in der tmp.txt-Datei geschaut.
Ist in dieser ein Datum schon erhalten, dann wird dies auch als Startdatum genutzt. Ist sie jedoch leer,
wird das Standard-Startdatum (05.01.2020) gesetzt. Beim Enddatum handelt es sich immer um die aktuelle Zeit der Abfrage.
"""
def get_start_and_end_date():

    try:
        if not os.path.exists(dateTmpFile):
            open(dateTmpFile, "w")

        tmp = open(dateTmpFile, "r")
        startDate = tmp.read()

        if startDate == "":
            startDate = "2020-01-05T00:00:00Z"
        tmp.close()

        return startDate

    except:
        raise file_exception("Unzureichende Lese- und Schreibrechte.")

"""
ZIP-Datei vom DWD wird heruntergeladen, die CSV darin wird ausgelesen, 
und die einzelnen Temperaturdaten werden in ein Array mit ihren dazugehörigen Zeitstempeln gelagert.
"""
def get_temp_data(url):

    returnData = []

    try:
        response = requests.get(url)
        zip_file = ZipFile(BytesIO(response.content))
        files = zip_file.namelist()

    except:
        raise url_exception("Die URL ist fehlerhaft.")

    with zip_file.open(files[0]) as csvfile:   

        data = pd.read_csv(csvfile, encoding='utf8', sep=";")
        temperatures = data['TT_10']
        timestamp = data['MESS_DATUM']

        for i in range(len(temperatures)):

            element = [str(timestamp[i]), str(temperatures[i])]
            returnData.append(element)

    return returnData

"""
Temperaturdaten aus der extrahierten CSV-Datei werden für die InfluxDB passend formatiert, 
in ein JSON-Array gespeichert und zurückgegeben.
"""
def get_dwd_data(url):

    jsonWeatherArray = []
    temperatures = get_temp_data(url)
    startDatumGefunden = False
    lastDateRead = ""
    
    try:

        for i in range(len(temperatures)):

            if get_timestamp_dwd(temperatures[i][0]) == get_start_and_end_date():
                startDatumGefunden = True

            if startDatumGefunden:

                timeString = get_timestamp_dwd(temperatures[i][0])
                jsonBody = [
                    {'measurement': 'temperaturDWD',
                    "time": utils.get_converted_date(timeString),
                    "fields":{"temperature":float(temperatures[i][1])}
                    }
                ]

                jsonWeatherArray.append(jsonBody)

            lastDateRead = get_timestamp_dwd(temperatures[i][0])

    except:
        raise raw_data_exception("Übergebenes Array fehlerhaft.")

    
    try:
        tmp = open(dateTmpFile, "w")
        tmp.write(lastDateRead)
        tmp.close()

    except:
        raise file_exception("Unzureichende Lese- und Schreibrechte.")

    return jsonWeatherArray

""""
Main-Methode für den Hauptaufruf.
""""
def historische_daten_erheben(url):

    utils.write_to_influx(get_dwd_data(url))