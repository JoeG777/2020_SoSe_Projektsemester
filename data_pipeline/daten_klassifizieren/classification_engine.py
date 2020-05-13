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
    """Name in documentation: klassifizierer_anwenden()
    Marks the occurrences of the selected event in the data with the use of the classifier
    :param
        config: Contains parameters for classifying the data
    :raises
    :return
        int: Status code that indicates whether the marking was successful(0 Success, 1 Failure)"""
    trainingsdata_editing_engine.enrich_data(config)
    datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement, \
     datasource_raw_data, measurement_raw, register_dict = get_config_parameter(config)
    start = convert_time(timeframe[0])
    end = convert_time(timeframe[1])
    df_query = read_manager.read_query(datasource_enriched_data, f"SELECT * FROM {measurement} WHERE time >= {start}ms "
                                                                 f"AND time <= {end}ms")
    model = model_persistor.load_classifier(config)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    df_query = df_query.drop(df_query.index[-1])
    df_query = df_query.drop(df_query.index[0])
    classified_data_df = df_query.copy()
    classified_data_df[selected_event] = model.predict(df_query)

    df_raw = read_manager.read_query('test', f"SELECT * FROM {measurement_raw} WHERE time >= {start}ms AND time "
                                                   f"<= {end}ms")
    df_raw = df_raw.drop(df_raw.index[-1])
    df_raw = df_raw.drop(df_raw.index[0])
    df_raw[selected_event] = classified_data_df[selected_event]
    write_manager.write_dataframe(datasource_classified_data, df_raw, measurement)
    return 0


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param
        config: dictionary from which the parameters will be extracted
    :raises
    :return
        int: #########################"""
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
    """Convert a given date and time to unix timestamp
   :param
       time_var: date and time to convert
   :raises
   :return
       int: The converted time as unix timestamp"""
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000
