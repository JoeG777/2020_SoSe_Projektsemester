import pandas as pd
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
from data_pipeline.daten_klassifizieren.training_data_time_points import event_start_end_timestamp as markers
from datetime import datetime
import time
import data_pipeline.exception.exceptions as ex
from data_pipeline.daten_klassifizieren.classification_API import logger


def enrich_data(config):
    """Name in documentation: daten_erweitern()
    Enrich data to include values to be able to train the classifier or to classify the data afterwards

    :raises InvalidConfigValueException: Raised if a value inside of the config is wrong
    :raises InvalidConfigKeyException :Raised if a key in the config does not exist
    :raises DBException: if there are problems with the database connection
    :return int: Status code that indicates whether the enriching was successful(0 Success, 1 Failure)"""
    try:
        selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
        required_registers, datasource_enriched_data, datasource_marked_data, \
        start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
        del_marker, end_ch, measurement_enriched, events, datasource_predicted_data, measurement_predicted = get_config_parameter(config)
    except Exception as e:
        raise ex.InvalidConfigKeyException("Key " + str(e) + " was not found in config")
    try:
        start = convert_time(start_time)
        end = convert_time(end_time)
    except Exception as e:
        raise ex.InvalidConfigValueException(str(e))
    counter = 0
    try:
        if selected_event == 'standard':
            df_query = read_manager.read_query(datasource_raw_data, f"SELECT * FROM {measurement_raw} WHERE time >= {start}ms AND time <= {end}ms")
        if selected_event == 'pred':
            df_query = read_manager.read_query(datasource_predicted_data, f"SELECT * FROM {measurement_predicted} WHERE time >= {start}ms AND time <= {end}ms")
        df_query = df_query.astype('float64')
        if 'historic_weatherdata' in df_query.columns:
            df_query = df_query.drop(['historic_weatherdata'], axis=1)
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info('raw_data loaded')
    for register in required_registers:
        if register_dict[register] not in df_query.columns:
            raise ex.InvalidConfigValueException(register_dict[register] + ' not found in dataframe columns')
        df_query[f'{register_dict[register]}_deriv'] = (df_query[f'{register_dict[register]}'].shift(-1) -
                                                        (df_query[f'{register_dict[register]}'].shift(1))) / 2
        df_query[f'{register_dict[register]}_pct_ch'] = df_query[f'{register_dict[register]}'].pct_change(1)
        df_query[f'{register_dict[register]}_ch_abs'] = df_query[f'{register_dict[register]}'].diff(1)
        '''
        df_query[f'{register_dict[register]}_diff'] = df_query[f'{register_dict[register]}'] - \
                                                      df_query[f'{register_dict[register]}'].shift(-1)
                                                      test for warmwassermarker'''
        df_query[f'{register_dict[register]}_diff'] = df_query[f'{register_dict[register]}'] - \
                                                      df_query[f'{register_dict[register]}'].shift(-1)
        if counter == 0:
            df = df_query
            counter += 1
        else:
            df[f'{register_dict[register]}'] = df_query[f'{register_dict[register]}']
            df[f'{register_dict[register]}_deriv'] = df_query[f'{register_dict[register]}_deriv']
            df[f'{register_dict[register]}_pct_ch'] = df_query[f'{register_dict[register]}_pct_ch']
            df[f'{register_dict[register]}_ch_abs'] = df_query[f'{register_dict[register]}_ch_abs']
            df[f'{register_dict[register]}_diff'] = df_query[f'{register_dict[register]}_diff']
    try:
        write_manager.write_dataframe(datasource_enriched_data, df, selected_event)
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info(f'enriched_data for {measurement_enriched} successfully persisted')
    return 0


def mark_data(config):
    """
    Name in documentation: daten_markieren()
    Mark the data with the occurrences of the selected event

    :raises InvalidConfigValueException :Raised if a value inside of the config is wrong
    :raises InvalidConfigKeyException :Raised if a key in the config does not exist
    :raises DBException :if there are problems with the database connection
    :return int: Status code that indicates whether the marking was successful(0 Success, 1 Failure)
    """
    try:
        selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
        required_registers, datasource_enriched_data, datasource_marked_data, \
        start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
        del_marker, end_ch, measurement_enriched, events, datasource_predicted_data, measurement_predicted = get_config_parameter(config)
    except Exception as e:
        raise ex.InvalidConfigKeyException("Key " + str(e) + " was not found in config")
    try:
        start = convert_time(start_time)
        end = convert_time(end_time)
    except Exception as e:
        raise ex.InvalidConfigValueException(str(e))
    try:
        df = read_manager.read_query(datasource_enriched_data, f"SELECT * FROM {selected_event} WHERE time >= {start}ms AND time <= {end}ms")
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info('enriched_data loaded')
    #if selected_event == 'standard':
    for event in events:
        spaces = 0
        df[f"{event}_marker"] = 0.0  # Spalte des Event initialisieren
        points_for_event = markers[event]  # dictionary für das event holen
        for key in points_for_event.keys():
            if (str(df.index[0]) < key < str(df.index[-1])) and (str(df.index[0]) < points_for_event[key] < str(df.index[-1])):  # überprüfen, ob key und value im Dataframe sind
                df.loc[key, f"{event}_marker"] = 1.0  # key ist der Startpunkt
                df.loc[points_for_event[key], f"{event}_marker"] = -1.0  # value ist Endpunkt
            # TODO: Warnung oder Exception, wenn keine Punkte für den aktuellen Zeitraum
            # TODO: noch testen mit realen Daten, bisher nur mit Dumps
        spaces = df.loc[(df[f"{event}_marker"] == 1.0) | (df[f"{event}_marker"] == -1.0)].index.tolist()
        df[event] = 0.0
        if (len(spaces) % 2) == 1:
            raise ex.InvalidConfigValueException('unable to create correct trainingsdata for this timeframe with given event values')
        for i in range(0, len(spaces), 2):
            df.loc[spaces[i]:spaces[i+1], event] = 1.0
    try:
        write_manager.write_dataframe(datasource_marked_data, df, selected_event)
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info(f"marked_data for {selected_event} successfully persisted")
    return 0


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param config classification_config: dictionary from which the parameters will be extracted
    :return string: selected_event: selected classification event
    :return string: datasource_raw_data: database name for the enriched data
    :return string: measurement_raw: measurement for the raw_data
    :return string: datasource_enriched_data: database name for the enriched data
    :return string: datasource_marked_data: database name for the marked data
    :return string: start_time: start time for the query of the required data
    :return string: end_time: end time for the query of the required data
    :return string: register_dict: list of all the register
    :return string: required_registers: list of required registers needed for the data editing
    :return float: start_deriv: threshold value for derivation to indicate a start point
    :return float: start_evap: threshold value for evaporation column in dataframe
    :return float: start_marker: value to indicate the start point of an event
    :return float: end_deriv: threshold value for derivation to indicate a ending point
    :return float: end_deriv_n3: threshold value for derivation of 3 rows to indicate a ending point
    :return float: end_marker: value to indicate the end point of an event
    :return float: start_ch: threshold value for change_column in dataframe
    :return float: start_abtau: threshold value to check if a abtauzyklus starts
    :return float: end_shift:
    :return float: del_marker: value for the deletion marker in the classificated column
    :return float: end_ch
        """
    selected_event = config['selected_event']
    datasource_raw_data = config['datasource_raw_data']['database']
    measurement_raw = config['datasource_raw_data']['measurement']
    measurement_enriched = config['datasource_enriched_data']['measurement']
    datasource_enriched_data = config['datasource_enriched_data']['database']
    datasource_marked_data = config['datasource_marked_data']['database']
    datasource_predicted_data = config['datasource_predicted_data']['database']
    start_time = config['timeframe'][0]
    end_time = config['timeframe'][1]
    register_dict = config['register_dict']
    required_registers = config[f"{selected_event}_register"]
    start_deriv = config['event_features']['start_deriv']
    start_evap = config['event_features']['start_evap']
    start_marker = config['event_features']['start_marker']
    end_deriv = config['event_features']['end_deriv']
    end_deriv_n3 = config['event_features']['end_deriv_n3']
    end_marker = config['event_features']['end_marker']
    start_ch = config['event_features']['start_ch']
    start_abtau = config['event_features']['start_abtau']
    end_shift = config['event_features']['end_shift']
    del_marker = config['event_features']['del_marker']
    end_ch = config['event_features']['end_ch']
    events = config[selected_event]
    measurement_predicted = config['datasource_predicted_data']['measurement']
    return selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
           required_registers, datasource_enriched_data, datasource_marked_data,\
           start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
           del_marker, end_ch, measurement_enriched, events, datasource_predicted_data, measurement_predicted


def convert_time(time_var):
    """Convert a given date and time to unix timestamp
   :param time_var: date and time to convert
   :return int: The converted time as unix timestamp"""
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000


if __name__ == "__main__":
    enrich_data()
    mark_data()
