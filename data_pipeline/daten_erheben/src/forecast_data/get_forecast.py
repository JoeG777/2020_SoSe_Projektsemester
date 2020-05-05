from urllib.request import urlopen
import urllib.request
from zipfile import ZipFile
import xml.etree.ElementTree as et
import data_pipeline.daten_erheben.src.utils.utils as utils
from data_pipeline.daten_erheben.src.exception import file_exception, url_exception, raw_data_exception
import data_pipeline.daten_erheben.src.log_writer as log_writer

logger = log_writer.LogWriter()

def get_forecast_data(url):

    '''
    The KML-file including the forecast weatherdata is being processed as XML. The Method searches and saves the Temperature data,
    transform it for InfluxDB and Changes the type from Kelvin to Celsius. The formatted forecast temperature data is saved in one Json-Array.
    The Method returns this Array.
    :param url: This is the URL to download the forecast weatherdata.
    :return: Returns a JSON-Array existing of forecast temperature data.
    :raises raw_data_exception: For incorrect passed data.
    '''

    tree = et.parse(get_forecast(url)) # XML-Dokument in XML-Tree umwandeln
    root = tree.getroot() # XML-Dokument in XML-Tree umwandeln

    timestamps = []
    timestampsFormatted = []
    temperatures = []
    data = []

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

    # Timestamps umformatieren (YYYY-MM-DDT00:00:00.000Z -> YYYY-MM-DDT00:00:00Z)
    for i in timestamps:
        timestampsFormatted.append(i[:19] + "Z")

    # 2D-Array bestehend aus Tupeln mit je einem Timestamp und einer Temperaturmessung zusammensetzen
    for i in range(len(temperatures)):
        data.append([timestampsFormatted[i], temperatures[i]])
        
    jsonWeatherArray = []

    try:

        for i in range(len(data)):

            jsonBody = [
                {'measurement': 'temperaturForecastDWD',
                "time": utils.get_converted_date(data[i][0]),
                "fields":{"temperatureForecast":(float(data[i][1])-273.15)} # Umrechnung von Kelvin zu Celsius (°C = K - 273,15)
                }
            ]

            jsonWeatherArray.append(jsonBody)

    except:
        logger.influx_logger.error("Datenarray fehlerhaft.")
        raise raw_data_exception("Datenarray fehlerhaft.")

    return jsonWeatherArray


def get_forecast(url):

    '''
    This Method downloads the KMZ file from the URL, saves it as ZIP-file and extracts it.
    :param url: This is the URL to download the forecast weatherdata.
    :return: The return is a list of all files in the saved ZIP-file.
    :raises file_exception: For inadequate read and write rights.
    :raises url_exception: For incorrect URL.
    '''

    try:
        urllib.request.urlretrieve(url, "data.zip") # KMZ-Datei herunterladen und als .zip speichern

    except:
        logger.influx_logger.error("Die URL ist fehlerhaft.")
        raise url_exception("Die URL ist fehlerhaft.")

    try:
        with ZipFile('data.zip', 'r') as zip_datei:
            filename = zip_datei.namelist()[0] # Liste aller Dateien in der gespeicherten ZIP-Datei ermitteln 
            zip_datei.extractall("") # ZIP-Datei entpacken 

    except:
        logger.influx_logger.error("Unzureichende Lese- und Schreibrechte.")
        raise file_exception("Unzureichende Lese- und Schreibrechte.")

    return filename


def vorhersage_daten_erheben(url):

    '''
    Main-method for the main call.
    '''

    utils.write_to_influx(get_forecast_data(url))