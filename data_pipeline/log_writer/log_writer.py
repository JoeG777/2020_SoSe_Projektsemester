from influx_logging import InfluxHandler
import logging

class LogWriter():

    def __init__(self):

        self.influx_handler = InfluxHandler(database="error_log")
        logging.getLogger().setLevel(logging.DEBUG)

        self.influx_logger = logging.getLogger('influx_logging.tests.simple_message')
        self.influx_logger.addHandler(self.influx_handler)



