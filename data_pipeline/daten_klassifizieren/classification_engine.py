import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import sklearn
import data_pipeline.daten_klassifizieren.model_persistor as model_persistor
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata_editing_engine
import data_pipeline.db_connector.src.read_manager.read_manager as read_manager
import data_pipeline.db_connector.src.write_manager.write_manager as write_manager
import data_pipeline.exception.exceptions as ex
from datetime import datetime
import time
from data_pipeline.daten_klassifizieren.classification_API import logger

def apply_classifier(config):
    """Name in documentation: klassifizierer_anwenden()
    Marks the occurrences of the selected event in the data with the use of the classifier
    :param config: Contains parameters for classifying the data
    :raises ConfigTypeException

    :return int: Status code that indicates whether the classifying was successful(0 Success, 1 Failure)"""
    logger.info("starting classification...")
    if not isinstance(config, dict):
        raise ex.ConfigTypeException("Wrong data structure of configuration: " + str(config))

    trainingsdata_editing_engine.enrich_data(config)
    logger.info("data enriched...")
    datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement, \
    datasource_raw_data, measurement_raw = get_config_parameter(config)

    logger.info("Fetched relevant data...")

    start = convert_time(timeframe[0])
    end = convert_time(timeframe[1])

    try:
        df_query = read_manager.read_query(datasource_enriched_data, f"SELECT * FROM {selected_event} WHERE time >= {start}ms "
                                                                    f"AND time <= {end}ms")
    except Exception:
        raise ex.DBException("Exception in read_manager")

    model = model_persistor.load_classifier(config)
    logger.info("Model geladen...")
    #letzte und erste Reihe mit NaN weil kein Wert nachher und kein Wert vorher zur Berechnung der zusätzl Merkmale
    try:
        df_query = df_query.drop(df_query.index[-1])
        df_query = df_query.drop(df_query.index[0])
    except IndexError:
        raise ex.DBException('Wrong query')


    classified_data_df = df_query.copy()

    try:
        classified_data_df[selected_event] = model.predict(df_query)
        logger.info("Daten klassifiziert...")
    except sklearn.exceptions.NotFittedError:
        raise ex.SklearnException("Classifier not fitted")
    except ValueError:
        raise ex.SklearnException("Input contains NaN, infinity or a value too large for dtype('float64')")

    df_raw = read_manager.read_query('test', f"SELECT * FROM {measurement_raw} WHERE time >= {start}ms AND time "
                                                   f"<= {end}ms")
    df_raw = df_raw.drop(df_raw.index[-1])
    df_raw = df_raw.drop(df_raw.index[0])

    df_raw[selected_event] = classified_data_df[selected_event]
    print(classified_data_df[selected_event].sum())
    try:
        write_manager.write_dataframe(datasource_classified_data, df_raw, measurement)
        logger.info("Daten persistiert. Klassifizierung abgeschlossen")
    except Exception:
        raise ex.DBException("Exception in write_manager")

    return 0


def get_config_parameter(config):
    """Extract relevant parameters from the config dictionary
    :param config: Dictionary from which the parameters will be extracted
    :raises ConfigException Raised if parameters from the config are wrong or missing
    :return datasource_enriched_data Database from which values​calculated from the data are loaded
    :return datasource_classified_data Database for the classified data
    :return datasource_raw_data Database from which data are loaded to be classified
    :return timeframe Period of time
    :return selected_event Scheduled event
    :return measurement Measurement from Database of the selected event
    :return measurement_raw Measurement from Database that contains raw data"""
    try:
        datasource_enriched_data = config['datasource_enriched_data']['database']
        datasource_classified_data = config['datasource_classified_data']['database']
        timeframe = config['timeframe']
        selected_event = config['selected_event']
        measurement = config['datasource_classified_data']['measurement']
        datasource_raw_data = config['datasource_raw_data']['database']
        measurement_raw = config['datasource_raw_data']['measurement']
    except Exception:
        raise ex.ConfigException("Missing or wrong parameters in config")

    return datasource_enriched_data, datasource_classified_data, timeframe, selected_event, measurement, \
        datasource_raw_data, measurement_raw


def convert_time(time_var):
    """Convert a given date and time to unix timestamp
   :param time_var: date and time to convert
   :raises InvalidConfigValueException Raised if the parameter timeframe from the config is wrong
   :return int: The converted time as unix timestamp"""
    try:
        time_var = datetime.strptime(time_var, "%Y-%m-%d %H:%M:%S.%f %Z")
    except Exception:
        raise ex.InvalidConfigValueException("Timeframe value in Config wrong")

    return int((time.mktime(time_var.timetuple())))*1000

if __name__ == "__main__":
    apply_classifier(config)