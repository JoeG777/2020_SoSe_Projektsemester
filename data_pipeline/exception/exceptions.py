class RedundantConfigException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'RedundantConfigException: {0}'.format(self.message)
        else:
            return 'RedundantConfigException has been raised'


class IncompleteConfigException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'IncompleteConfigException: {0}'.format(self.message)
        else:
            return 'IncompleteConfigException has been raised'


class InconsistentConfigException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InconsistentConfigException: {0}'.format(self.message)
        else:
            return 'InconsistentConfigException has been raised'


class InvalidTrainingPercentageException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InvalidTrainingPercentageException: {0}'.format(self.message)
        else:
            return 'InvalidTrainingPercentageException has been raised'


class InvalidConfigException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InvalidConfigException: {0}'.format(self.message)
        else:
            return 'InvalidConfigException has been raised'#


class PersistorException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'PersistorException: {0}'.format(self.message)
        else:
            return 'PersistorException has been raised'


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