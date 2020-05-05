"""
Die File-Exception wird geworfen, wenn eine Datei lokal nicht gefunden werden kann, oder man keine Schreibe-/Leserechte in dem jeweiligen Verzeichnis besitzt.
"""
class file_exception(Exception):

    def __init__(self, *args):

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FileException, {0}'.format(self.message)
        else:
            return 'FileException'

"""
Die URL-Exception wird geworfen, wenn die übergebene URL fehlerhaft ist und die benötigten Wetterdaten daher nicht heruntergeladen werden können. 
"""
class url_exception(Exception):

    def __init__(self, *args):

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UrlException, {0}'.format(self.message)
        else:
            return 'UrlException'

"""
Die Raw-Data-Exception wird geworfen, wenn bspw. das Array mit den Tupeln aus Timestamp und Temperaturmesspunkt fehlerhaft aufgebaut ist und von der jeweigen Methode daher nicht genutzt werden kann. 
"""
class raw_data_exception(Exception):

    def __init__(self, *args):

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'RawDataException, {0}'.format(self.message)
        else:
            return 'RawDataException'

