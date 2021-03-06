from datetime import datetime
import data_pipeline.db_connector.src.write_manager.write_manager as wm
import pytz
import data_pipeline.exception.exceptions as exc
from data_pipeline.front_end_interface.src.front_end_interface_api.front_end_interface_api import logger

def get_current_time_utc():
    '''
    Name in documentation: 'get_current_time'
    This method sets the timezone of the timestamp to UTC in order to show it correctly in Grafana.
    :return: the date 2 hours before the passed date.
    '''

    local_timezone = pytz.timezone("Europe/Berlin")
    timezone = pytz.timezone("UTC")

    local_timestemp = local_timezone.localize(datetime.now())
    timezone_timestamp = local_timestemp.astimezone(timezone)

    return str(timezone_timestamp)[:10] + "T" + str(timezone_timestamp)[11:19] + "Z"


def format_json(json):
    '''
    Name in documentation: 'formatiere_eingabedaten()'
    Formats the Json-File for InfluxDB
    :param json: Nilan-Ventilation Unit Parameters
    '''
    try:
        json_nilan = [
            {'measurement': 'steuerungsparameter',
             "time": get_current_time_utc(),
             "fields": {
                 "temperatur": json['raumtemperatur'],
                 "zuluft_stufe": json['luefterstufe_zuluft'],
                 "abluft_stufe": json['luefterstufe_abluft'],
                 "modus": json['betriebsmodus']
                 }
             }
        ]
    except:
        logger.influx_logger.error('Config-JSON incomplete')
        raise exc.RawDataException('Config-JSON incomplete', 905)

    return json_nilan


def write_to_nilan(json):
    '''
    Name in documentation: 'schreibe_eingabedaten()'
    Writes the User-Settings into Nilan-Ventilation Unit
    :param json: Nilan-Ventilation Unit Parameters
    :raises
    '''

    try:
        wm.write_query("db_steuerungsparameter", format_json(json))

    except:
        logger.influx_logger.error('Writing data to database was unsuccessful')
        raise exc.DBException('Writing data to database was unsuccessful', 901)
