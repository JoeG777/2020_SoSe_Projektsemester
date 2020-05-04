import pandas

def interpolieren(config, zyklenfreie_daten):

    # Abklären wie nur pro Zyklus Interpoliert werden kann. Ansonsten pro Kurve und dann nochmal Config ändern!

    zyklenfreie_daten['room'].interpolate(method = config["room"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )
    zyklenfreie_daten['condenser'].interpolate(method = config["condenser"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )
    zyklenfreie_daten['evaporator'].interpolate(method = config["evaporator"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )
    zyklenfreie_daten['inlet'].interpolate(method = config["inlet"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )
    zyklenfreie_daten['outlet'].interpolate(method = config["outlet"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )
    zyklenfreie_daten['freshAirIntake'].interpolate(method = config["freshAirIntake"]["WarmWasserZyklus"]["Interpolation"] , inplace = True )

    return zyklenfreie_daten