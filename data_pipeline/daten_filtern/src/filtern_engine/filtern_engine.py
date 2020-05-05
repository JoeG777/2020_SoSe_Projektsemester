import pandas
import numpy as np
from data_pipeline.exception.exceptions import DBException, ConfigExeption
import data_pipeline.log_writer.log_writer as log_writer
import data_pipeline.db_connector.src.read_manager.read_manager as reader
import data_pipeline.db_connector.src.write_manager.write_manager as writer
from influxdb import InfluxDBClient
from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config



logger = log_writer.LogWriter()

def filtern():
    """
    Name in documentation: 'filtern'
    Takes the config and load the klassified data. After that it delete and interpolate the marked intervall. Last it persist the filtered data.
    :raises ConfigExeption: If the config is wrong.
    :return: A http status code.
    """

    config = filtern_config["filter_options"][filtern_config["selected_value"]]

    filtern_data = get_data()

    try:
        for kurve in config:
            for zyklus in config[kurve]:
                if config[kurve][zyklus]["delete"] == "True":
                    filtern_data = tag_drop(zyklus, kurve, filtern_data)
                    methode = config[kurve][zyklus]["Interpolation"]
                    filtern_data = interpolation(methode, kurve, filtern_data)

    except:
        logger.influx_logger.error("Config is wrong.")
        raise ConfigExeption("Config is wrong.", 900)


    persist_data(filtern_data)
    pass
    #return statuscode


def get_data():
    """
    Name in documentation: 'get_data'
    Load the klassified data.
    :return: The klassified data
    """
    try:
        # TODO Query für klassifizierte Daten
        klassifizierte_daten = reader.read_query("Klassifizierte Daten", "KOMPLETTE KLASSIFIZIERTE DATEN!")
    except:
        logger.influx_logger.error("Database not available.")
        raise DBException("Database not available.", 901)


def tag_drop(kurve, zyklus, filtern_data):
    """
    Name in documentation: 'tag_drop'
    Delete one cycle in one curve.
    :param kurve: the name of the curve as string
    :param zyklus: the name of the cycle as string
    :param filtern_data: the klassified data
    :return: the klassified data with one cycle of one curve deleted
    """

    filtern_data = filtern_data.loc[filtern_data.zyklus == True , kurve] = np.nan

    return filtern_data


def interpolation(methode, kurve, zyklenfreie_daten):
    """
    Name in documentation: 'interpolation'
    Interpolate one curve, after a cycle was deletet. The method has already been read from config file.
    :param methode: The interpolation method as string.
    :param kurve: the name of the curve as string.
    :param zyklenfreie_daten: the klassified data with deleted fields.
    :return: The klassified data after filtering a cycle.
    """

    gefilterte_daten = zyklenfreie_daten[kurve].interpolate(method = methode , inplace = True)

    return gefilterte_daten

def persist_data(filtern_data):
    '''
    Name in documentation: 'persist_data'
    Persist the filtered data.
    :param filtern_data: the filtered data.
    :return: A http status code.
    '''
    try:
        # TODO Query für klassifizierte Daten
        writer.write_query("Gefilterte Daten" , filtern_data)
    except:
        logger.influx_logger.error("Database not available.")
        raise DBException("Database not available.", 901)

    pass


