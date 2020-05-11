from datetime import datetime
import data_pipeline.db_connector.src.write_manager.write_manager.py as wm
import pytz

def get_current_time_utc():

    '''
    Name in documentation: ''
    Writes the User-Settings into
    :raises
    '''

    local_timezone = pytz.timezone("Europe/Berlin")
    timezone = pytz.timezone("UTC")

    local_timestemp = local_timezone.localize(datetime.now())
    timezone_timestamp = local_timestemp.astimezone(timezone)

    return str(timezone_timestamp)[:10] + "T" + str(timezone_timestamp)[11:19] + "Z"

def format_json(json):

    '''
    Name in documentation: 'formatiere_eingabedaten()'
    Writes the User-Settings into
    :param json: Download-link for the weather data from DWD
    :raises
    '''

    json_nilan_array = [
        {'measurement': 'raumtemperatur',
         "time": get_current_time_utc(),
         "fields":{"temperatur":json['raumtemperatur']}
         },
        {'measurement': 'luefterstufe_zuluft',
         "time": get_current_time_utc(),
         "fields":{"stufe":json['luefterstufe_zuluft']}
         },
        {'measurement': 'luefterstufe_abluft',
         "time": get_current_time_utc(),
         "fields":{"stufe":json['luefterstufe_abluft']}
         },
        {'measurement': 'betriebsmodus',
         "time": get_current_time_utc(),
         "fields":{"modus":json['betriebsmodus']}
         }
    ]

    return json_nilan_array

def write_to_nilan(json):

    '''
    Name in documentation: 'schreibe_eingabedaten()'
    Writes the User-Settings into Nilan-Ventilation Unit
    :param json:
    :raises
    '''

    wm.write_to_influx_json("db_steuerungsparameter", format_json(json))



