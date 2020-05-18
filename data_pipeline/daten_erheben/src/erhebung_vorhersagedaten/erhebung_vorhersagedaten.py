from urllib.request import urlopen
import urllib.request
from zipfile import ZipFile
import xml.etree.ElementTree as et
import data_pipeline.daten_erheben.src.utils.utils as utils
from data_pipeline.exception.exceptions import FileException, UrlException, RawDataException
import data_pipeline.log_writer.log_writer as logger
import pandas as pd

logger = logger.Logger("logs", "logs", "uipserver.ddns.net", 8086,"Datenerhebung")

def get_forecast_data(url):
    '''
    Name in documentation: 'get_forecast_data'
    The KML-file including the forecast weatherdata is being processed as XML. The Method searches and saves the Temperature data,
    transform it for InfluxDB and Changes the type from Kelvin to Celsius. The formatted forecast temperature data is saved in one Json-Array.
    The Method returns this Array.
    :param url: This is the URL to download the forecast weatherdata.
    :raises RawDataException: For incorrect passed data.
    :return: Returns a JSON-Array existing of forecast temperature data.
    '''

    tree = et.parse(get_forecast(url)) # XML-Dokument in XML-Tree umwandeln
    root = tree.getroot() # XML-Dokument in XML-Tree umwandeln

    timestamps = []
    timestamps_formatted = []
    temperatures = []
    data = []

    try:
        for element in root:
            for child in element:
                for grandchild in child:
                    for grandgrandchild in grandchild.findall('{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}Forecast'): # Nur durch jende children Iterieren, welche den Tag 'Forecast' besitzen
                        if grandgrandchild.attrib['{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}elementName'] == "T5cm": # Das Element finden, welches das Attribut "T5cm" besitzt
                            for grandgrandgrandchild in grandgrandchild:
                                for i in range(len(grandgrandgrandchild.text.split("     "))-1):
                                    temperatures.append(float(grandgrandgrandchild.text.split("     ")[i+1]))
                    for grandgrandchild in grandchild:
                        for grandgrandgrandchild in grandgrandchild:
                            if grandgrandgrandchild.tag == "{https://opendata.dwd.de/weather/lib/pointforecast_dwd_extension_V1_0.xsd}TimeStep": # Das Element finden, welches den Tag "TimeStemp" besitzt
                                for i in grandgrandgrandchild.text.split(" "):
                                    timestamps.append(i)

        # Format Timestamps (YYYY-MM-DDT00:00:00.000Z -> YYYY-MM-DDT00:00:00Z)
        for i in timestamps:
            timestamps_formatted.append(i[:19] + "Z")

        # 2D-Array consisting out of tuples of a timestamp and temperature_data, each
        for i in range(len(temperatures)):
            data.append([timestamps_formatted[i], temperatures[i]])

    except:
        logger.influx_logger.error("Incorrect file format.")
        raise FileException("Incorrect file format.", 903)

    try:

        headers = ['time', 'temperature']

        weather_data = []

        for i in range(len(data)):

            field = [utils.get_converted_date(data[i][0]), float(data[i][1])-273.15]
            weather_data.append(field)

        df = pd.DataFrame(weather_data, columns=headers)
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')


    except:
        logger.influx_logger.error("incorrect passed data.")
        raise RawDataException("incorrect passed data.", 905)

    return df


def get_forecast(url):
    '''
    Name in documentation: 'get_forecast'
    This Method downloads the KMZ file from the URL, saves it as ZIP-file and extracts it.
    :param url: This is the URL to download the forecast weatherdata.
    :raises FileException: For inadequate read and write rights.
    :raises UrlException: For incorrect URL.
    :return: The return is a list of all files in the saved ZIP-file.
    '''

    try:
        urllib.request.urlretrieve(url, "data.zip") # KMZ-Datei herunterladen und als .zip speichern

    except:
        logger.influx_logger.error("Incorrect URL.")
        raise UrlException("Incorrect URL.", 904)

    try:
        with ZipFile('data.zip', 'r') as zip_datei:
            filename = zip_datei.namelist()[0] # Liste aller Dateien in der gespeicherten ZIP-Datei ermitteln 
            zip_datei.extractall("") # ZIP-Datei entpacken 

    except:
        logger.influx_logger.error("Inadequate read and write rights.")
        raise FileException("Inadequate read and write rights.", 903)

    return filename


def raise_forecast_data(url):
    '''
    Name in documentation: 'vorhersagedaten_erheben'
    Main-method for the main call.
    :param url: This is the URL to download the forecast weather data.
    '''

    utils.write_to_influx(get_forecast_data(url))