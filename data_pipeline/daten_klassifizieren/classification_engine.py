import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import sklearn
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata_editing_engine
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.log_writer as log_writer
from data_pipeline.daten_klassifizieren.config import classification_config as config
from datetime import datetime
import time


# TODO: pre processing in daten erweitern, damit anwendungsdaten selbes format wie trainingsdaten haben
# TODO: daten erweitern mit np.array
# TODO: ergebnis von predict wahrscheinlich array, das man wieder in df umwandeln muss zum speichern
def apply_classifier(config):
    trainingsdata_editing_engine.enrich_data(config)
    datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement, \
     datasource_raw_data, measurement_raw, register_dict = get_config_parameter(config)
    start = convert_time(timeframe[0])
    end = convert_time(timeframe[1])
    df_query = read_manager.read_query(datasource_enriched_data, f"SELECT * FROM {measurement} WHERE time >= {start}ms "
                                                                 f"AND time <= {end}ms")

    #df_query = read_manager.read_data(datasource_enriched_data, measurement=measurement,
                                      #start_utc=str(start), end_utc=str(end))
    model = model_persistor.load_classifier(config)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    #df_query.dropna(inplace=True)
    df_query = df_query.drop(df_query.index[-1])
    classified_data_df = df_query.copy()
    classified_data_df[selected_event] = model.predict(df_query)

    #print(classified_data_df.loc[classified_data_df[selected_event]])
    counter = 0
    for register in register_dict:
        df_raw = read_manager.read_data(datasource_raw_data, measurement=measurement_raw, register=register,
                                        start_utc=str(start), end_utc=str(end))
        df_raw = df_raw.drop(df_raw.index[-1])
        df_raw = df_raw.drop(labels='register', axis=1)
        if counter == 0:
            df_return = df_raw.rename(columns={'temperature': f'{register_dict[register]}'})
            counter += 1
        else:
            df_return[f'{register_dict[register]}'] = df_raw.rename(columns={'temperature': f'{register_dict[register]}'})
    df_return['abtauzyklus'] = classified_data_df['abtauzyklus']
    write_manager.write_dataframe(datasource_classified_data, df_return, measurement)
    return 0


def get_config_parameter(config):
    datasource_enriched_data = config['datasource_enriched_data']['database']
    datasource_classified_data = config['datasource_classified_data']['database']
    timeframe = config['timeframe']
    selected_event = config['selected_event']
    measurement = config['selected_event']
    datasource_raw_data = config['datasource_raw_data']['database']
    measurement_raw = config['datasource_raw_data']['measurement']
    register_dict = config['register_dict']
    return datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement, \
        datasource_raw_data, measurement_raw, register_dict


def convert_time(time_var):
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000
