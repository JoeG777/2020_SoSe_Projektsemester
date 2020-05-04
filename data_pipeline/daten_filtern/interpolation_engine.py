import pandas

def interpolieren(config, zyklenfreie_daten):
    zyklenfreie_daten['room'].interpolate(method = config["room"]["Interpolation"] , inplace = True )
    return zyklenfreie_daten