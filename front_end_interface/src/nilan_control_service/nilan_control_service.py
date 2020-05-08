from datetime import datetime
import data_pipeline.db_connector.src.write_manager.write_manager.py as wm
import pytz

def get_current_time_utc():

    local_timezone = pytz.timezone("Europe/Berlin")
    timezone = pytz.timezone("UTC")

    local_timestemp = local_timezone.localize(datetime.now())
    timezone_timestamp = local_timestemp.astimezone(timezone)

    return str(timezone_timestamp)[:10] + "T" + str(timezone_timestamp)[11:19] + "Z"

def write_to_nilan(json):

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

    wm.write_to_influx_json(json_nilan_array)



