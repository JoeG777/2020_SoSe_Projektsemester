import pandas

def interpolieren(config, kurve,zyklus,  zyklenfreie_daten):
    '''
    Name in documentation: 'interpolieren'
    :param config:
    :param zyklenfreie_daten:
    :return: filterd data
    '''

    zyklenfreie_daten[kurve].interpolate(method = config[kurve][zyklus]["Interpolation"] , inplace = True)

    return zyklenfreie_daten