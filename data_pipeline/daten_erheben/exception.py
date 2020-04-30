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

