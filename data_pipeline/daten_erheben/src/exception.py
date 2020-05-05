class FileException(Exception):

    """
    Gets thrown once a local file cannot be found, or the user does not have the necessary rights to read or write.
    """

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


class UrlException(Exception):

    """
    Gets thrown once the passed URL is incorrect and therefore the neccessary weather data can't get pulled.
    """

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


class RawDataException(Exception):

    """
    Gets thrown once for example the array out of timestamps and temperaturedata is defective and therefore can't be used by the respective method.
    """

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

