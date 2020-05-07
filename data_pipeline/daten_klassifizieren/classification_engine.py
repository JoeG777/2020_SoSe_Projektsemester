import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import sklearn
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager as write_manager
import data_pipeline.log_writer as log_writer
from data_pipeline.daten_klassifizieren.config import classification_config as config
from datetime import datetime

# TODO: pre processing in daten erweitern, damit anwendungsdaten selbes format wie trainingsdaten haben
# TODO: daten erweitern mit np.array
# TODO: ergebnis von predict wahrscheinlich array, das man wieder in df umwandeln muss zum speichern
def apply_classifier(config):
    datasource_raw_data, datasource_classified_data, timeframe, selected_event, measurement, register \
        = get_config_parameter(config)
    raw_data_df = read_manager.read_register_of_measurement_from_to(str(datasource_raw_data), str(measurement),
                                                                    str(register), str(timeframe[0]), str(timeframe[1]))
    print(raw_data_df.head(50))
    model = model_persistor.load_classifier(config)
    classified_data_df = raw_data_df.copy()
    data_array = [[37.543878, -1.399388 ,  41.003469, -0.001514, 0.001709, -0.000388, -0.015931, -0.002388, -0.010312, -0.002827],
                  [37.530816, -1.402653, 40.998776, -0.000348, 0.002333, -0.000114, -0.004694, -0.003265, 0.008665, 0.006194]
        ,   [37.601200,  -1.387000, 41.020800,  0.001875, -0.011160, 0.000537,  0.022024 , 0.015653,  0.018469,  0.029898]]
    test = model.predict(data_array) #classified_data_df[selected_event] = model.predict(classified_data_df)
    print(test)
    #classified_data_json = classified_data_df.to_json()
    #print(classified_data_json)
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

