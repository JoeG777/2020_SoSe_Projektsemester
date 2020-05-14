from influx_logging import InfluxHandler
import logging
import inspect

class Logger():

    def __init__(self, database, measurement, host, port, component):
        """
        Constructor of the custom logger.
        :param database: database to write the logs into
        :param measurement: measurement to write the logs into
        :param host: host of the db server
        :param port: port of the db server
        :param component: the component the logger is writing from, e.g. 'Prediction Engine'
        """
        self.COMPONENT = component
        self.influx_handler = InfluxHandler(database=database,
                                            measurement=measurement,
                                            host=host, port=port,
                                            extra_fields="component"
                                            )
        logging.getLogger().setLevel(logging.DEBUG)
        self.influx_logger = logging.getLogger('influx_logging')
        self.influx_logger.addHandler(self.influx_handler)

    def info(self, message):
        """
        Wrapper for standard info message.
        :param message: the message to write
        """
        filename = self.get_calling_filename()
        self.influx_logger.info(message, extra={"component": self.COMPONENT, "file": filename})

    def warning(self, message):
        """
        Wrapper for standard warning message.
        :param message: the message to write
        """
        filename = self.get_calling_filename()
        self.influx_logger.warning(message, extra={"component": self.COMPONENT, "file": filename})

    def error(self, message):
        """
        Wrapper for standard error message.
        :param message: the message to write
        """
        filename = self.get_calling_filename()
        self.influx_logger.error(message, extra={"component": self.COMPONENT, "file": filename})

    def write_into_measurement(self, measurement, content):
        """
        Used to write a info message into a different measurement.
        :param measurement: The measurement the info message should be written into.
        :param content: The content of the info message to be written.
        """
        filename = self.get_calling_filename()
        default_measurement = self.influx_handler.measurement
        self.influx_handler.measurement = measurement
        self.influx_logger.info(content, extra={"component": self.COMPONENT, "file": filename})
        self.influx_handler.measurement = default_measurement

    def get_calling_filename(self):
        """
        Gets the filename of the file in which the logging function is called from.
        :return: the filename of the file in which the logging function is called from or an alternate message if the
        filename could not be retrieved
        """
        try:
            frame = inspect.stack()[2]
            module = inspect.getmodule(frame[0])
            return module.__file__
        except:
            return "File name could not be retrieved"




