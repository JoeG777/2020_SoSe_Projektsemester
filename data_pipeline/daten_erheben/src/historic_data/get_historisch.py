from zipfile import ZipFile
import os
import requests
from io import BytesIO
import pandas as pd
import data_pipeline.daten_erheben.src.utils.utils as utils
from data_pipeline.daten_erheben.src.exception import FileException, UrlException, RawDataException
import data_pipeline.daten_erheben.src.log_writer as log_writer

dateTmpFile = "/tmp/tmp.txt"
logger = log_writer.LogWriter()


def get_timestamp_dwd(time):
    '''
    Formats the time stamp of the individual weather data in a suitable format for writing into InfluxDB.
    :param time: unformatted time stamp of the individual weather data
    :return: formatted time stamp
    '''

    formatted = time[:4] + "-" + time[4:6] + "-" + time[6:8] + "T" + time[8:10] + ":" + time[10:12] + ":00Z"
    return formatted


def get_start_date():
    '''
    Requests the start of the weather data.
    To determine the start date, it looks for an entry in the tmp.txt file.
    If a date has already been received in this, then this is also used as the start date.
    However, if it is empty, the standard start date (05.01.2020) is set.
    :raises file_exception: For inadequate read and write rights.
    :return: start date for the beginning of the query
    '''

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
        logger.influx_logger.error("Unzureichende Lese- und Schreibrechte.")
        raise FileException("Unzureichende Lese- und Schreibrechte.")


def get_temp_data(url):
    '''
    Downloads the ZIP file from DWD, reads the CSV,
    and stores the individual temperature data in an array with their associated time stamps.
    :param url: Download-link for the weather data from DWD
    :raises url_exception: For incorrect URL.
    :return: Array with all weather entries and their time stamps
    '''

    returnData = []

    try:
        response = requests.get(url)
        zip_file = ZipFile(BytesIO(response.content))
        files = zip_file.namelist()

    except:
        logger.influx_logger.error("Die URL ist fehlerhaft.")
        raise UrlException("Die URL ist fehlerhaft.")

    with zip_file.open(files[0]) as csvfile:   

        data = pd.read_csv(csvfile, encoding='utf8', sep=";")
        temperatures = data['TT_10']
        timestamp = data['MESS_DATUM']

        for i in range(len(temperatures)):

            element = [str(timestamp[i]), str(temperatures[i])]
            returnData.append(element)

    return returnData


def get_dwd_data(url):
    '''
    Temperature data from the extracted CSV file are formatted appropriately for the InfluxDB,
    stored in a JSON array and returned.
    :param url: Download-link for the weather data from DWD
    :raises raw_data_exception: For incorrect passed data
    :raises file_exception: For inadequate read and write rights.
    :return: Json-Array with all the formatted weather entries and their formatted time stamps
    '''

    jsonWeatherArray = []
    temperatures = get_temp_data(url)
    startDatumGefunden = False
    lastDateRead = ""
    
    try:

        for i in range(len(temperatures)):

            if get_timestamp_dwd(temperatures[i][0]) == get_start_date():
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
        logger.influx_logger.error("Übergebenes Array fehlerhaft.")
        raise RawDataException("Übergebenes Array fehlerhaft.")

    
    try:
        tmp = open(dateTmpFile, "w")
        tmp.write(lastDateRead)
        tmp.close()

    except:
        logger.influx_logger.error("Unzureichende Lese- und Schreibrechte.")
        raise FileException("Unzureichende Lese- und Schreibrechte.")

    return jsonWeatherArray


def historische_daten_erheben(url):
    '''
    Main method for the main call.
    :param url: Download-link for the weather data from DWD
    '''

    utils.write_to_influx(get_dwd_data(url))