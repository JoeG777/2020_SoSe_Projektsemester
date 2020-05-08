from zipfile import ZipFile
import os
import requests
from io import BytesIO
import pandas as pd
import data_pipeline.daten_erheben.src.utils.utils as utils
from data_pipeline.exception.exceptions import FileException, UrlException, RawDataException
import data_pipeline.daten_erheben.src.log_writer as log_writer

date_tmp_file = "./data_pipeline/daten_erheben/src/erhebung_historischer_daten/tmp/datenerhebung_tmp.txt"
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
    :raises FileException: For inadequate read and write rights.
    :return: start date for the beginning of the query
    '''

    try:
        if not os.path.exists(date_tmp_file):
            open(date_tmp_file, "w")

        tmp = open(date_tmp_file, "r")
        start_date = tmp.read()

        if start_date == "":
            start_date = "2020-01-05T00:00:00Z"
        tmp.close()

        return start_date

    except:
        logger.influx_logger.error("Inadequate read and write rights.")
        raise FileException("Inadequate read and write rights.", 903)


def get_temp_data(url):
    '''
    Downloads the ZIP file from DWD, reads the CSV,
    and stores the individual temperature data in an array with their associated time stamps.
    :param url: Download-link for the weather data from DWD
    :raises UrlException: For incorrect URL.
    :return: Array with all weather entries and their time stamps
    '''

    return_data = []

    try:
        response = requests.get(url)
        zip_file = ZipFile(BytesIO(response.content))
        files = zip_file.namelist()

    except:
        logger.influx_logger.error("Incorrect URL.")
        raise UrlException("Incorrect URL.", 904)

    try:
        with zip_file.open(files[0]) as csvfile:

            data = pd.read_csv(csvfile, encoding='utf8', sep=";")
            temperatures = data['TT_10']
            timestamp = data['MESS_DATUM']

            for i in range(len(temperatures)):

                element = [str(timestamp[i]), str(temperatures[i])]
                return_data.append(element)

    except:
        logger.influx_logger.error("Inadequate read and write rights.")
        raise FileException("Inadequate read and write rights.", 903)

    return return_data


def find_start_date(temperatures):

    '''
    This method searches for the start-date of the query depending on the datenerhebung_tmp.txt-file.
    :param temperatures: Holds the weather data.
    :return: Start-date for the query.
    '''
    
    try:

        for i in range(len(temperatures)):

            if get_timestamp_dwd(temperatures[i][0]) == get_start_date():

                start_date = i

    except:
        logger.influx_logger.error("incorrect passed data.")
        raise RawDataException("incorrect passed data.", 905)

    return start_date


def get_dwd_data(url):

    '''
    Temperature data from the extracted CSV file are formatted appropriately for the InfluxDB,
    stored in a JSON array and returned.
    :param url: Download-link for the weather data from DWD
    :raises RawDataException: For incorrect passed data
    :raises FileException: For inadequate read and write rights.
    :return: Json-Array with all the formatted weather entries and their formatted time stamps
    '''

    try:
        temperatures = get_temp_data(url)
        json_weather_array = []
        for counter in range(find_start_date(temperatures), len(temperatures)):

            time_string = get_timestamp_dwd(temperatures[counter][0])
            jsonBody = [
                {'measurement': 'temperatur_DWD',
                 "time": utils.get_converted_date(time_string),
                 "fields":{"temperature":float(temperatures[counter][1])}
                 }
            ]

            json_weather_array.append(jsonBody)

            last_date_read = get_timestamp_dwd(temperatures[counter][0])
        tmp = open(date_tmp_file, "w")
        tmp.write(last_date_read)
        tmp.close()

    except FileException:
        logger.influx_logger.error("Inadequate read and write rights.")
        raise FileException("Inadequate read and write rights.", 903)

    except UrlException:
        logger.influx_logger.error("Incorrect URL.")
        raise UrlException("Incorrect URL.", 904)

    return json_weather_array

def raise_historic_data(url):
    '''
    Name in documentation: 'historische_daten_erheben()'
    Main method for the main call.
    :param url: Download-link for the weather data from DWD
    '''

    utils.write_to_influx(get_dwd_data(url))