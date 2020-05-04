from zipfile import ZipFile
import os
import requests
from io import BytesIO
import pandas as pd
import data_pipeline.daten_erheben.utils as utils
from data_pipeline.daten_erheben.exception import file_exception, url_exception, raw_data_exception
import data_pipeline.daten_erheben.log_writer as logger

dateTmpFile = "/tmp/tmp.txt"

def get_timestamp_dwd(time):

    formatted = time[:4] + "-" + time[4:6] + "-" + time[6:8] + "T" + time[8:10] + ":" + time[10:12] + ":00Z"
    return formatted

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

def historische_daten_erheben(url):

    utils.write_to_influx(get_dwd_data(url))