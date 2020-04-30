import tag_drop_engine
import interpolation_engine

def filtern(config):
    klassifizierte_daten = get_data()

    zyklenfreie_daten = tag_drop(config, klassifizierte_daten)

    gefilterte_daten = interpolate(config, zyklenfreie_daten)

    persist_data(gefilterte_daten)

def get_data():
    klassifizierte_daten = []
    return klassifizierte_daten

def tag_drop(config , klassifizierte_daten):
    zyklenfreie_daten = tag_drop_engine.intervall_löschen(config, klassifizierte_daten)
    return zyklenfreie_daten

def interpolate(config, zyklenfreie_daten):
    gefilterte_daten = interpolation_engine.interpolieren(config, zyklenfreie_daten)
    return gefilterte_daten

def persist_data(gefilterte_daten):
    print("gut")