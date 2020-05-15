import numpy as np
from data_pipeline.log_writer.log_writer import Logger
import data_pipeline.exception.exceptions as exe
import data_pipeline.db_connector.src.read_manager.read_manager as reader
import data_pipeline.db_connector.src.write_manager.write_manager as writer
from datetime import datetime
import time

#logger = Logger()

def filter(config, timeframe):
    '''
    Name in documentation: 'filtern'
    Takes the config and load the klassified data. After that it delete and interpolate the marked intervall. Last it persist the filtered data.
    :raises ConfigExeption: If the config is wrong.
    '''

    filtern_data = get_data(timeframe)


    try:
        for curve in config:
            for cycle in config[curve]:
                if config[curve][cycle]["delete"] == "True":
                    filtern_data = tag_drop(curve, cycle, filtern_data)
                    method = config[curve][cycle]["Interpolation"]
                    filtern_data = interpolation(method, curve, filtern_data)

        print("Gefilterte Daten:")
        print(filtern_data.loc[filtern_data.abtauzyklus == True])

    except exe.ConfigException:
        raise exe.ConfigException("Filtern Config format is not correct.", 900)


    persist_data(filtern_data)


def get_data(timeframe):
    """
    Name in documentation: 'get_data'
    Load the klassified data.
    :raises DBExeption: If the Database is not aviable.
    :return: The klassified data
    """
    try:
        classified_data = reader.read_data('nilan_classified' ,measurement = 'abtauzyklus' ,
                                           start_utc= str(convert_time(timeframe[0])),
                                           end_utc= str(convert_time(timeframe[1])),
                                           )

        print("Get_Data Ausgabe:")
        print(classified_data)
        print("________________________________")

        print("Get_Data Ausgabe nur True-gesetzte:")
        print(classified_data.loc[classified_data.abtauzyklus == True]) #only True cycle
        print("________________________________")


    except exe.DBException:
        #logger.influx_logger.error("Database not available.")
        raise exe.DBException("Database is not available. Get_data() failed", 901)

    return classified_data


def tag_drop(curve, cycle, filtern_data):
    '''
    Name in documentation: 'tag_drop'
    Delete one cycle in one curve.
    :param curve: the name of the curve as string
    :param cycle: the name of the cycle as string
    :param filtern_data: the klassified data
    :raises ConfigExeption: If the config is wrong.
    :return: the klassified data with one cycle of one curve deleted
    '''

    try:
        filtern_data.loc[filtern_data[cycle] == True, curve] = np.NaN

        print("Tag_Drop:")
        print(curve)
        print(filtern_data.loc[filtern_data.abtauzyklus == True][curve])
        print("________________________________")

    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Filtern Config format is not correct. Tag_drop() failed", 900)

    return filtern_data


def interpolation(methode, curve, zyklenfreie_daten):
    '''
    Name in documentation: 'interpolation'
    Interpolate one curve, after a cycle was deletet. The method has already been read from config file.
    :param methode: The interpolation method as string.
    :param kurve: the name of the curve as string.
    :param zyklenfreie_daten: the klassified data with deleted fields.
    :raises ConfigExeption: If the config is wrong.
    :return: The klassified data after filtering a cycle.
    '''
    try:
        zyklenfreie_daten[curve] = zyklenfreie_daten[curve].interpolate(method= methode, order = 3)

        print("Interpoliert:")
        print(zyklenfreie_daten.loc[zyklenfreie_daten.abtauzyklus == True][curve])
        print("________________________________")

    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Filtern Config format is not correct. Interpolation() failed.", 900)

    return zyklenfreie_daten


def persist_data(filtern_data):
    '''
    Name in documentation: 'persist_data'
    Persist the filtered data.
    :param filtern_data: the filtered data.
    :raises DBExeption: If the Database is not aviable.
    '''

    try:
        writer.write_dataframe('filtered_data', filtern_data, measurement = 'temperature_register')

        print("Persistiert")
        print("________________________________")

    except:
        #logger.influx_logger.error("Database not available.")
        raise exe.DBException("Database is not available. Persist_data() failed", 901)




def convert_time(time_var):
    '''
    Convert the time UTC.
    :param time_var:
    :return: the converted time.
    '''
    try:
        time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
        return int((time.mktime(time_var.timetuple())))*1000
    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Filtern Config format is not correct. Convert_time() failed", 900)

'''

def configure_data(filter_data):

    time = None
    for i in filter_data:
        if filter_data.at[filter_data.index[i],filter_data.columns[1]] == True and filter_data.at[filter_data.index[i+1],filter_data.columns[1]] == False:
            filter_data.at[filter_data.index[i+1],filter_data.columns[1]] = 5
            filter_data.at[filter_data.index[i+2],filter_data.columns[1]] = 7
            i = i+3

    return filter_data
'''