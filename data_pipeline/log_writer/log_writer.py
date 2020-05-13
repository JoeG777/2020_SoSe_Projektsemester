from influx_logging import InfluxHandler
import logging


class Logger():

    def __init__(self, database='logs', measurement='logs', host='localhost', port=8086):
        self.influx_handler = InfluxHandler(database=database, measurement=measurement, host=host, port=port)
        logging.getLogger().setLevel(logging.DEBUG)
        self.influx_logger = logging.getLogger('influx_logging')
        self.influx_logger.addHandler(self.influx_handler)
