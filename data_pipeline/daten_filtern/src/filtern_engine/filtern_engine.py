
import pandas as pd
import numpy as np
from data_pipeline.log_writer.log_writer import Logger
from data_pipeline.exception.exceptions import DBException, ConfigException
import data_pipeline.db_connector.src.read_manager.read_manager as reader
import data_pipeline.db_connector.src.write_manager.write_manager as writer
from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config
from datetime import datetime
import time

logger = Logger()
config = filtern_config["filter_options"][filtern_config["selected_value"]]
print(config)

def filter(config):
    """
    Name in documentation: 'filtern'
    Takes the config and load the klassified data. After that it delete and interpolate the marked intervall. Last it persist the filtered data.
    :raises ConfigExeption: If the config is wrong.
    :return: A http status code.
    """
    #statuscode = None
    filtern_data = get_data()

    #try:
    for curve in config:
        for cycle in config[curve]:
            if config[curve][cycle]["delete"] == "True":
                filtern_data = tag_drop(curve, cycle, filtern_data)
                method = config[curve][cycle]["Interpolation"]
                filtern_data = interpolation(method, curve, filtern_data)

    persist_data(filtern_data)
   # except:
        #logger.influx_logger.error("Config is wrong.")
        #raise ConfigException("Filtern Config is wrong.", 900)
        #statuscode = 900

    #statuscode = persist_data(filtern_data)

    #return statuscode


def get_data():

    df = reader.read_data('nilan_classified' ,measurement = 'abtauzyklus' , start_utc = str(convert_time('2020-01-14 00:00:00.000 UTC')), end_utc = str(convert_time('2020-01-15 12:0:00.000 UTC')))
    #print(df)
    print(df.loc[df.abtauzyklus == True])
    return df

    """
    Name in documentation: 'get_data'
    Load the klassified data.
    :return: The klassified data
    """
    #klassifizierte_daten = None
    #try:

    """
        roomQueryTemp = 'SELECT "valueScaled" FROM "temperature_register" WHERE register=\'210\' AND time >= 1582497763413ms and time <= 1582614984756ms'
        room = pd.DataFrame(client.query(roomQueryTemp).get_points())
        client.close()
        room['time'] = pd.to_datetime(room['time'], utc = True)
        room['WarmWasserZyklus'] = False
        room.loc[(room.time >= pd.Timestamp('2020-02-24 22:30:00').tz_localize('UTC')) & (room.time <= pd.Timestamp('2020-02-25 05:05:00').tz_localize('UTC')), 'WarmWasserZyklus'] = True
        room['time'] = pd.to_datetime(room['time'])
        room = room.set_index('time')
        room = room.rename(columns={'valueScaled' : 'room'})
    """


        #klassifizierte_daten = reader.read_data('klassifizierte_daten')
   # except:
        #logger.influx_logger.error("Database not available.")
        #raise DBException("Database not available.", 901)




def tag_drop(curve, cycle, filtern_data):
    """
    Name in documentation: 'tag_drop'
    Delete one cycle in one curve.
    :param curve: the name of the curve as string
    :param cycle: the name of the cycle as string
    :param filtern_data: the klassified data
    :return: the klassified data with one cycle of one curve deleted
    """

    filtern_data.loc[filtern_data[cycle] == True, curve] = np.NaN
    print(filtern_data.loc[filtern_data.abtauzyklus == True])
    return filtern_data


def interpolation(methode, curve, zyklenfreie_daten):
    """
    Name in documentation: 'interpolation'
    Interpolate one curve, after a cycle was deletet. The method has already been read from config file.
    :param methode: The interpolation method as string.
    :param kurve: the name of the curve as string.
    :param zyklenfreie_daten: the klassified data with deleted fields.
    :return: The klassified data after filtering a cycle.
    """

    zyklenfreie_daten[curve] = zyklenfreie_daten[curve].interpolate(method= methode, order = 3)
    print(zyklenfreie_daten.loc[zyklenfreie_daten.abtauzyklus == True])
    return zyklenfreie_daten


def persist_data(filtern_data):
    '''
    Name in documentation: 'persist_data'
    Persist the filtered data.
    :param filtern_data: the filtered data.
    :return: A http status code.
    '''
    statuscode = None
    #try:
    writer.write_dataframe('filtered_data', filtern_data, measurement = 'temperature_register')
    print("GUUUUUUUUT")
        #statuscode = 200
    #except:
        #logger.influx_logger.error("Database not available.")
        #statuscode = 901
        #raise DBException("Database not available.", 901)

    #return statuscode


def convert_time(time_var):
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000

filter(config)