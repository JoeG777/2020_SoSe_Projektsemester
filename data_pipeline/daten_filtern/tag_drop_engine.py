import pandas
import numpy as np

def intervall_loeschen(config, klassifizierte_daten):

    if config["room"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'roomTemp'] = np.nan
    if config["room"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'roomTemp'] = np.nan
    if config["room"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'roomTemp'] = np.nan
    if config["room"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'roomTemp'] = np.nan

    if config["condenser"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'condenserTemp'] = np.nan
    if config["condenser"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'condenserTemp'] = np.nan
    if config["condenser"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'condenserTemp'] = np.nan
    if config["condenser"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'condenserTemp'] = np.nan

    if config["evaporator"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'evaporatorTemp'] = np.nan
    if config["evaporator"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'evaporatorTemp'] = np.nan
    if config["evaporator"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'evaporatorTemp'] = np.nan
    if config["evaporator"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'evaporatorTemp'] = np.nan

    if config["inlet"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'inletTemp'] = np.nan
    if config["inlet"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'inletTemp'] = np.nan
    if config["inlet"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'inletTemp'] = np.nan
    if config["inlet"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'inletTemp'] = np.nan

    if config["outlet"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'outletTemp'] = np.nan
    if config["outlet"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'outletTemp'] = np.nan
    if config["outlet"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'outletTemp'] = np.nan
    if config["outlet"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'outletTemp'] = np.nan

    if config["freshAirIntake"]["WarmWasserZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.WarmWasserTag == True , 'freshAirIntakeTemp'] = np.nan
    if config["freshAirIntake"]["OfenZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.OfenTag == True , 'freshAirIntakeTemp'] = np.nan
    if config["freshAirIntake"]["LüfterZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.LuefterTag == True , 'freshAirIntakeTemp'] = np.nan
    if config["freshAirIntake"]["AbtauZyklus"]["delete"] == "True":
        klassifizierte_daten.loc[klassifizierte_daten.AbtauTag == True , 'freshAirIntakeTemp'] = np.nan

    return klassifizierte_daten