import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import sklearn
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
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
    datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement \
        = get_config_parameter(config)
    start = convert_time(timeframe[0])
    end = convert_time(timeframe[1])
    df_query = read_manager.read_data(datasource_enriched_data, measurement='training',
                                      start_utc=str(start), end_utc=str(end))
    print(df_query.columns)
    model = model_persistor.load_classifier(config)
    classified_data_df = df_query.copy()
    classified_data_df[selected_event] = model.predict(df_query)
    pd.set_option('display.max_rows', None)
    print(classified_data_df.loc[classified_data_df['abtauzyklus']==True])
    write_manager.write_dataframe(datasource_classified_data, classified_data_df, measurement)
    return 0


def get_config_parameter(config):
    datasource_enriched_data = config['datasource_enriched_data']['database']
    datasource_classified_data = config['datasource_classified_data']['database']
    timeframe = config['timeframe']
    selected_event = config['selected_event']
    measurement = config['selected_event']
    return datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement


def convert_time(time_var):
    time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    return int((time.mktime(time_var.timetuple())))*1000

apply_classifier(config)

