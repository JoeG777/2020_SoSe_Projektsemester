"""
Gets thrown once a local file cannot be found, or the user does not have the necessary rights to read or write.
"""
class FileException(Exception):

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
Gets thrown once the passed URL is incorrect and therefore the neccessary weather data can't get pulled. 
"""
class UrlException(Exception):

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
Gets thrown once for example the array out of timestamps and temperaturedata is defective and therefore can't be used by the respective method. 
"""
class RawDataException(Exception):

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

