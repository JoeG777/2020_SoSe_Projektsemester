import pandas as pd
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
from datetime import datetime
import time
import data_pipeline.exception.exceptions as ex
from data_pipeline.daten_klassifizieren.classification_API import logger


def enrich_data(config):
    """Name in documentation: daten_erweitern()
    Enrich data to include values to be able to train the classifier or to classify the data afterwards
    :param
        config: Contains parameters for enriching the data
    :raises
    :return
        int: Status code that indicates whether the enriching was successful(0 Success, 1 Failure)"""
    try:
        selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
        required_registers, datasource_enriched_data, datasource_marked_data, \
        start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
        del_marker = get_config_parameter(config)
    except Exception as e:
        raise ex.InvalidConfigKeyException("Key " + str(e) + " was not found in config")
    try:
        start = convert_time(start_time)
        end = convert_time(end_time)
    except Exception as e:
        raise ex.InvalidConfigValueException(str(e))
    counter = 0
    try:
        df_query = read_manager.read_query(datasource_raw_data, f"SELECT * FROM temperature_register WHERE time >= {start}ms AND time "
                                                f"<= {end}ms")
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
    logger.info(f'enriched_data for {selected_event} successfully persisted')
    return 0


def mark_data(config):
    """Name in documentation: daten_markieren()
    Mark the data with the occurrences of the selected event
    :param
        config: Contains parameters for marking the data
    :raises
    :return
        int: Status code that indicates whether the marking was successful(0 Success, 1 Failure)"""
    try:
        selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
        required_registers, datasource_enriched_data, datasource_marked_data, \
        start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
        del_marker = get_config_parameter(config)
    except Exception as e:
        raise ex.InvalidConfigKeyException("Key " + str(e) + " was not found in config")
    try:
        start = convert_time(start_time)
        end = convert_time(end_time)
    except Exception as e:
        raise ex.InvalidConfigValueException(str(e))
    try:
        df = read_manager.read_query(datasource_enriched_data, f"SELECT * FROM {selected_event} WHERE time >= {start}ms "
                                                         f"AND time <= {end}ms")
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info('enriched_data loaded')
    if selected_event == 'abtauzyklus':
        #df['abtaumarker'] = 0
        #df.loc[(df['evaporator_deriv']>= start_deriv) & (df['evaporator_deriv'].shift(1) < start_deriv) & (df['evaporator'] <= start_evap), 'abtaumarker'] = start_marker
        #df.loc[(abs(df['evaporator_deriv']) <= end_deriv) & (df['evaporator_deriv'].shift(3) < end_deriv_n3), 'abtaumarker'] = end_marker
        pd.set_option("display.max_rows", None)
        df['abtauzyklus_marker'] = 0.0
        df.loc[df['condenser_diff'] > 4, 'abtauzyklus_marker'] = 1
        df.loc[df['condenser_diff'] < -4, 'abtauzyklus_marker'] = -1
        df.loc[(df['abtauzyklus_marker'] == 1) & (df['abtauzyklus_marker'].shift(1) == 1), 'abtauzyklus_marker'] = 0
        df.loc[(df['abtauzyklus_marker'] == -1) & (df['abtauzyklus_marker'].shift(-1) == -1), 'abtauzyklus_marker'] = 0
        #df.loc[df['abtaumarker'].shift(1) == end_marker, 'abtaumarker'] = 0
        df['abtauzyklus'] = False
        spaces = df.loc[(df['abtauzyklus_marker'] == start_marker) | (df['abtauzyklus_marker'] == end_marker)].index.tolist()
        if (len(spaces) % 2) == 1:
            raise ex.InvalidConfigValueException('unable to create correct trainingsdata for this timeframe with given event values')
        for i in range(0, len(spaces), 2):
            df.loc[spaces[i]:spaces[i+1], 'abtauzyklus'] = True
    elif selected_event == 'warmwasseraufbereitung':
        df['warmwassermarker'] = 0.0
        '''df.loc[(df['inlet'].shift(1) > start_abtau) & (df['room_deriv'] <= start_deriv) & (df['room_deriv'] <= start_ch), 'warmwassermarker'] = start_marker

        df.loc[(df['warmwassermarker'] == start_marker) & ((df['warmwassermarker'].shift(-1) == start_marker) |
                                                           (df['warmwassermarker'].shift(-2) == start_marker)), 'warmwassermarker'] = del_marker

        df.loc[df['room_deriv'].shift(end_shift) >= end_deriv, 'warmwassermarker'] = end_marker

        df.loc[(df['warmwassermarker'] == end_marker) & ((df['warmwassermarker'].shift(-1) == end_marker) |
                                                         (df['warmwassermarker'].shift(-2) == end_marker)), 'warmwassermarker'] = del_marker

        df.loc[(df['warmwassermarker'].index.hour > 8) & (df['warmwassermarker'].index.hour < 22), 'warmwassermarker'] = 0'''

        df.loc[df['room_diff'] > 0.3, 'warmwassermarker'] = 1.0
        df.loc[df['room_diff'] < -0.26, 'warmwassermarker'] = -1.0

        df.loc[(df.index.hour > 10) & (df.index.hour < 20), 'warmwassermarker'] = 0.0
        spaces = df.loc[(df['warmwassermarker'] == start_marker) | (df['warmwassermarker'] == end_marker)].index.tolist()
        #for i in range(0, len(spaces), 2):
            #df.loc[spaces[i]:spaces[i+1], 'warmwasserzyklus'] = True
    else:
        raise ex.InvalidConfigValueException(selected_event + ' not an valid classification event')
    try:
        write_manager.write_dataframe(datasource_marked_data, df, selected_event)
    except Exception as e:
        raise ex.DBException(str(e))
    logger.info(f"marked_data for {selected_event} successfully persisted")
    return 0


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param
        config: dictionary from which the parameters will be extracted
    :raises
    :return
        string: selected_event: selected classification event
        string: datasource_raw_data: database name for the enriched data
        string: measurement_raw: measurement for the raw_data
        string: datasource_enriched_data: database name for the enriched data
        string: datasource_marked_data: database name for the marked data
        string: start_time: start time for the query of the required data
        string: end_time: end time for the query of the required data
        string: register_dict: list of all the register
        string: required_registers: list of required registers needed for the data editing
        float: start_deriv: threshold value for derivation to indicate a start point
        float: start_evap: threshold value for evaporation column in dataframe
        float: start_marker: value to indicate the start point of an event
        float: end_deriv: threshold value for derivatoin to indicate a ending point
        float: end_deriv_n3: threshold value for derivation of 3 rows to indicate a ending point
        float: end_marker: value to indicate the end point of an event
        float: start_ch: threshold value for change_column in dataframe
        float: start_abtau: threshold value to check if a abtauzyklus starts
        float: end_shift:
        float: del_marker: value for the deletion marker in the classificated column
        """
    selected_event = config['selected_event']
    datasource_raw_data = config['datasource_raw_data']['database']
    measurement_raw = config['datasource_raw_data']['measurement']
    datasource_enriched_data = config['datasource_enriched_data']['database']
    datasource_marked_data = config['datasource_marked_data']['database']
    start_time = config['timeframe'][0]
    end_time = config['timeframe'][1]
    register_dict = config['register_dict']
    required_registers = config[selected_event]
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
    return selected_event, datasource_raw_data, measurement_raw, start_time, end_time, register_dict, \
           required_registers, datasource_enriched_data, datasource_marked_data,\
           start_deriv, start_evap, start_marker, end_deriv, end_deriv_n3, end_marker, start_ch, start_abtau, end_shift, \
           del_marker


def convert_time(time_var):
    """Convert a given date and time to unix timestamp
   :param
       time_var: date and time to convert
   :raises
   :return
       int: The converted time as unix timestamp"""
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000

'''

 elif event == 'Warmwasseraufbereitung':
        #Parameter
        start_marker = config['event_features']['start_marker'] #1.0
        start_deriv = config['event_features']['start_deriv'] #-0.06
        start_ch = config['event_features']['start_ch'] #-0.06
        start_abtau = config['event_features']['start_abtau'] # 10.0
        end_marker = config['event_features']['end_marker'] #-1
        end_deriv = config['event_features']['end_deriv'] #0.06
        end_shift = config['event_features']['end_shift'] #30
        del_marker = config['event_features']['del_marker'] #10



        df['Warmwassermarker'] = 0
        #Markierung Anfang
        #durchschnittliche Ableitung Room <= -0.06
        df.loc[(df['In'].shift(1) > start_abtau) & (df['Room_deriv'] <= start_deriv) & (df['Room_deriv'] <= start_ch), 'Warmwassermarker'] = start_marker
        #Löschen doppelter oder dreifacher Startpunkte
        df.loc[(df['Warmwassermarker'] == start_marker) & ((df['Warmwassermarker'].shift(-1) == start_marker) |
                                                           (df['Warmwassermarker'].shift(-2) == start_marker)), 'Warmwassermarker'] = del_marker
        #Markierung Ende
        #durchschnittliche Ableitung Room <= 0.06
        df.loc[df['Room_deriv'].shift(end_shift) >= end_deriv, 'Warmwassermarker'] = end_marker
        #Löschen doppelter oder dreifacher Endpunkte
        df.loc[(df['Warmwassermarker'] == end_marker) & ((df['Warmwassermarker'].shift(-1) == end_marker) |
                                                         (df['Warmwassermarker'].shift(-2) == end_marker)), 'Warmwassermarker'] = del_marker
        #kann nur zwischen 22-8Uhr auftreten
        df.loc[(df['Warmwassermarker'].index.hour > 8) & (df['Warmwassermarker'].index.hour < 22), 'Warmwassermarker'] = 0

        #Zyklenbereich markieren
        spaces = df.loc[(df['Warmwassermarker'] == start_marker) | (df['Warmwassermarker'] == end_marker)].index.tolist()
        len(spaces)
        for i in range(0,len(spaces), 2):
            df.loc[spaces[i]:spaces[i+1], 'Warmwasserzyklus'] = True

    #DB-Connector.daten_schreiben(db_train, df)'''

if __name__ == "__main__":
    enrich_data(config)