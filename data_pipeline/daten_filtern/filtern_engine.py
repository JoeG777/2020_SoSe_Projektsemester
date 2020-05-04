import tag_drop_engine
import interpolation_engine

def filtern(config):
    '''
    Name in documentation: 'filtern'
    :param config:
    '''

    klassifizierte_daten = get_data()

    for kurve in config:
        for zyklus in config[kurve]:
            zyklenfreie_daten = tag_drop(config, zyklus, kurve, klassifizierte_daten)
            gefilterte_daten = interpolate(config, zyklus, kurve, zyklenfreie_daten)

    persist_data(gefilterte_daten)


def get_data():
    '''
    Name in documentation: 'get_data'
    :return: klassified data
    '''
    klassifizierte_daten = []
    return klassifizierte_daten


def tag_drop(config , kurve, zyklus, klassifizierte_daten):
    '''
    Name in documentation: 'tag_drop'
    :param config:
    :param klassifizierte_daten:
    :return: cycle free data
    '''
    zyklenfreie_daten = data_pipeline.daten_filtern.tag_drop_engine.intervall_löschen(config, kurve , zyklus, klassifizierte_daten)
    return zyklenfreie_daten


def interpolate(config, zyklenfreie_daten):
    '''
    Name in documentation: 'interpolate'
    :param config:
    :param zyklenfreie_daten:
    :return: filterd data
    '''
    gefilterte_daten = data_pipeline.daten_filtern.interpolation_engine.interpolieren(config, zyklenfreie_daten)
    return gefilterte_daten

def persist_data(gefilterte_daten):
    '''
    Name in documentation: 'persist_data'
    :param gefilterte_daten:
    '''
    print("gut")