class DataPipelineException(Exception):
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


class ConfigException(DataPipelineException):
    def __str__(self):
        if self.message:
            return 'ConfigException: {0}'.format(self.message)
        else:
            return 'ConfigException has been raised'


class IncompleteConfigException(ConfigException):
    def __str__(self):
        if self.message:
            return 'IncompleteConfigException: {0}'.format(self.message)
        else:
            return 'IncompleteConfigException has been raised'


class InconsistentConfigException(ConfigException):
    def __str__(self):
        if self.message:
            return 'InconsistentConfigException: {0}'.format(self.message)
        else:
            return 'InconsistentConfigException has been raised'


class InvalidTrainingPercentageException(ConfigException):
    def __str__(self):
        if self.message:
            return 'InvalidTrainingPercentageException: {0}'.format(self.message)
        else:
            return 'InvalidTrainingPercentageException has been raised'


class InvalidConfigKeyException(ConfigException):
    def __str__(self):
        if self.message:
            return 'InvalidConfigKeyException: {0}'.format(self.message)
        else:
            return 'InvalidConfigException has been raised'


class InvalidConfigValueException(ConfigException):
    def __str__(self):
        if self.message:
            return 'InvalidConfigValueException: {0}'.format(self.message)
        else:
            return 'InvalidConfigException has been raised'


class AmbiguousConfigException(ConfigException):
    def __str__(self):
        if self.message:
            return 'AmbiguousConfigException: {0}'.format(self.message)
        else:
            return 'AmbiguousConfigException has been raised'


class ConfigTypeException(ConfigException):
    def __str__(self):
        if self.message:
            return 'ConfigTypeException: {0}'.format(self.message)
        else:
            return 'ConfigTypeException has been raised'


class PersistorException(DataPipelineException):
    def __str__(self):
        if self.message:
            return 'PersistorException: {0}'.format(self.message)
        else:
            return 'PersistorException has been raised'


class DBException(DataPipelineException):
    def __str__(self):
        if self.message:
            return 'DBException: {0}'.format(self.message)
        else:
            return 'DBException has been raised'

class FileException(DataPipelineException): #author: Johannes, stand so in der Doku noch drinn...
    def __str__(self):
        if self.message:
            return 'FileExcpetion: {0}'.format(self.message)
        else:
            return 'FileExcpetion has been raised'

class SklearnException(DataPipelineException): #author: Johannes, stand so in der Doku noch drinn...
    def __str__(self):
        if self.message:
            return 'SklearnException: {0}'.format(self.message)
        else:
            return 'SklearnException has been raised'