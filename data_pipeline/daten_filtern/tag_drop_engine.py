import pandas
import numpy as np


"""
Auf Basis der in der Config Datei bestimmten Zyklen und Kurven und der mitgelieferten Daten, 
werden die entsprechenden Zyklenintervalle aus den Daten herausgelöscht, indem die Werte auf "Nan"
gesetzt werden. Die Parameter sind die klassifizierten Daten und die Config Datei. Als return Wert kommen 
die zyklenfreie Daten. 
"""

def intervall_loeschen(config, kurve , zyklus, klassifizierte_daten):
    '''
    Name in documentation: 'intervall_loeschen'
    :param config:
    :param klassifizierte_daten:
    :return: cycle free data
    '''

    if config[kurve][zyklus]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.zyklus == True , kurve] = np.nan

    return klassifizierte_daten