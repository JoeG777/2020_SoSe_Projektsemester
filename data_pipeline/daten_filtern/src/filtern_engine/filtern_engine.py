import pandas
import numpy as np


def filtern(config):
    """
    Name in documentation: 'filtern'
    Takes the config and load the klassified data. After that it delete and interpolate the marked intervall. Last it persist the filtered data.
    :param config: The seleceted value of filtern config.
    :return: A http status code.
    """

    filtern_data = get_data()

    for kurve in config:
        for zyklus in config[kurve]:
            if config[kurve][zyklus]["delete"] == "True":
                filtern_data = tag_drop(zyklus, kurve, filtern_data)
                methode = config[kurve][zyklus]["Interpolation"]
                filtern_data = interpolation(methode, kurve, filtern_data)

    persist_data(filtern_data)

    return statuscode


def get_data():
    """
    Name in documentation: 'get_data'
    Load the klassified data.
    :return: The klassified data
    """
    klassifizierte_daten = []
    return klassifizierte_daten


def tag_drop(kurve, zyklus, filtern_data):
    """
    Name in documentation: 'tag_drop'
    Delete one cycle in one curve.
    :param kurve: the name of the curve as string
    :param zyklus: the name of the cycle as string
    :param klassifizierte_daten: the klassified data
    :return: the klassified data with one cycle of one curve deleted
    """

    zyklenfreie_daten = klassifizierte_daten.loc[klassifizierte_daten.zyklus == True , kurve] = np.nan

    return zyklenfreie_daten


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
    # Aufruf DB-Connector
    statuscode = ""

    return statuscode


