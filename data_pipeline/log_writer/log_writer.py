from influx_logging import InfluxHandler
import logging


class Logger():

    def __init__(self, component, database='logs', measurement='logs', host='localhost', port=8086):
        self.COMPONENT = component
        self.influx_handler = InfluxHandler(database=database,
                                            measurement=measurement,
                                            host=host, port=port,
                                            extra_fields="component"
                                            )
        logging.getLogger().setLevel(logging.DEBUG)
        self.influx_logger = logging.getLogger('influx_logging')
        self.influx_logger.addHandler(self.influx_handler)

    def write_into_measurement(self, measurement, content):
        default_measurement = self.influx_handler.measurement
        self.influx_handler.measurement = measurement
        self.influx_logger.info(content, extra={"component": self.COMPONENT})
        self.influx_handler.measurement = default_measurement
