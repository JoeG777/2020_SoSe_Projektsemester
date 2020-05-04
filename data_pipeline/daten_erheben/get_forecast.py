from urllib.request import urlopen
import urllib.request
from zipfile import ZipFile
import xml.etree.ElementTree as et
import data_pipeline.daten_erheben.utils as utils
from data_pipeline.daten_erheben.exception import file_exception, url_exception, raw_data_exception
import data_pipeline.daten_erheben.log_writer as log_writer

"""
KML-Datei mit den Vorhersage-Wetterdaten wird als XML verarbeitet. Temperaturdaten der Vorhersagegröße werden gesucht und gespeichert.
Temperaturdaten werden für die InfluxDB passend formatiert, Temperatur von Kelvin in Grad Celsius umgerechnet und in einem JSON-Array gespeichert.
Gibt zusammengesetztes JSON-Array mit Vorhersage-Wetterdaten zurück.
"""
def get_forecast_data(url):

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
        raise raw_data_exception("Datenarray fehlerhaft.")

    return jsonWeatherArray

"""
Vorhersage-Wetterdaten-URL wird eingelesen. Die vorhandene KMZ-Datei wird als ZIP-Datei gespeichert und extrahiert.
Gibt Liste aller Dateien der gespeicherten ZIP-Datei zurück.
"""
def get_forecast(url):

    try:
        urllib.request.urlretrieve(url, "data.zip") # KMZ-Datei herunterladen und als .zip speichern

    except:
        raise url_exception("Die URL ist fehlerhaft.")

    try:
        with ZipFile('data.zip', 'r') as zip_datei:
            filename = zip_datei.namelist()[0] # Liste aller Dateien in der gespeicherten ZIP-Datei ermitteln 
            zip_datei.extractall("") # ZIP-Datei entpacken 

    except:
        raise file_exception("Unzureichende Lese- und Schreibrechte.")

    return filename

"""
Main-Methode für den Hauptaufruf.
"""
def vorhersage_daten_erheben(url):

    utils.write_to_influx(get_forecast_data(url))