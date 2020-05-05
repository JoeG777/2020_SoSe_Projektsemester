import pandas as pd
#import sklearn
#import LogWriter
#import DBConnector


def daten_erweitern(config):
    df = pd.DataFrame()
    event = config['selected_event']
    db_raw = config['datasource_raw_data']
    timeframe = config['timeframe']

    if event == 'Abtauzyklus':
        #evaporator = pd.Series(DB-Connector.daten_lesen(db_raw, 206, timeframe), index=Evaporator)
        #condensor = pd.Series(DB-Connector.daten_lesen(db_raw, 205, timeframe), index=Condensor)
        #df = pd.concat([evaporator, condensor], axis=1)
        #durchschnittliche Steigung an diesem Punkt
        df['Condensor_deriv'] = (df['Condensor'].shift(-1) - (df['Condensor'].shift(1))) / 2
        df['Evaporator_deriv'] = (df['Evaporator'].shift(-1) - (df['Evaporator'].shift(1))) / 2

    elif event == 'Warmwasseraufbereitung':
        #room = pd.Series(DB-Connector.daten_lesen(db_raw, 210, timeframe), index=Room)
        #df = pd.concat([room], axis=1)
        #durchschnittliche Ableitung
        df['Room_deriv'] = (df['Room'].shift(-1)-df['Room'].shift(1)) / 2
        #absolute Änderung
        df['Room_ch_abs'] = df['Room'].diff(1)



def daten_markieren(config):
    df = pd.DataFrame()
    event = config['selected_event']
    db_train = config['datasource_training_data']
    timeframe = config['timeframe']

    if event == 'Abtauzyklus':
        #Parameter
        start_marker = config['event_features']['start_marker']  #1.0
        start_deriv = config['event_features']['start_deriv']  #1.0
        start_evap = config['event_features']['start_evap']  #0.0
        end_marker = config['event_features']['end_marker']  #-1.0
        end_deriv = config['event_features']['end_deriv']  #0.5
        end_shift = config['event_features']['end_shift']  #-1.0
        del_marker = config['event_features']['del_marker']  #0.0

        df['Abtaumarker'] = 0
        #Markierung Anfang
        #durchschnittliche Steigung >= 1 & durchschnittliche Steigung davor < 1 & Temperatur Verdampfer <= 0
        df.loc[(df['Evaporator_deriv']>= start_deriv) & (df['Evaporator_deriv'].shift(1) < start_deriv) & (df['Evaporator'] <= start_evap), 'Abtaumarker'] = start_marker
        #Markierung Ende
        #absolute durchschnittliche Steigung <= 0.5 & durchschnittliche Steigung vor drei Messungen < -1.0
        df.loc[(abs(df['Evaporator_deriv']) <= end_deriv) & (df['Evaporator_deriv'].shift(3) < end_shift), 'Abtaumarker'] = end_marker
        # doppelte Endmarker raus
        df.loc[df['Abtaumarker'].shift(1) == end_marker, 'Abtaumarker'] = del_marker

        #Zyklenbereich markieren
        df['Abtauzyklus'] = False
        spaces = df.loc[(df['Abtaumarker'] == start_marker) | (df['Abtaumarker'] == end_marker)].index.tolist()
        len(spaces)
        for i in range(0, len(spaces), 2):
            df.loc[spaces[i]:spaces[i+1], 'Abtauzyklus'] = True

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

    #DB-Connector.daten_schreiben(db_train, df)