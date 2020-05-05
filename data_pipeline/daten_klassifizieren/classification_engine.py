import pandas as pd
import sklearn
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager as write_manager
import data_pipeline.log_writer as log_writer
from data_pipeline.daten_klassifizieren.config import classification_config as config
from datetime import datetime


def apply_classifier(config):
    datasource_raw_data, datasource_classified_data, timeframe, selected_event, measurement, register \
        = get_config_parameter(config)
    raw_data_df = read_manager.read_register_of_measurement_from_to(str(datasource_raw_data), str(measurement),
                                                                 str(register), str(timeframe[0]), str(timeframe[1]))
    print(raw_data_df.head(5))
    model = model_persistor.load_classifier(config)
    classified_data_df = raw_data_df.copy()
    print("hallo")
    #classified_data_df[selected_event] = model.predict(raw_data_df)
    #classified_data_json = classified_data_df.to_json()
    #write_manager.write_query_array(datasource_classified_data, classified_data_json)
    return 0


def get_config_parameter(config):
    datasource_raw_data = config['datasource_raw_data']
    datasource_classified_data = config['datasource_classified_data']
    timeframe = config['timeframe']
    timeframe_unix = (int(datetime.strptime(timeframe[0], "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
                      int(datetime.strptime(timeframe[1], "%Y-%m-%d %H:%M:%S").timestamp()) * 1000)
    selected_event = config['selected_event']
    measurement = config['measurement']
    register = config[selected_event]
    return datasource_raw_data, datasource_classified_data, timeframe_unix, selected_event, measurement, register


apply_classifier(config)
