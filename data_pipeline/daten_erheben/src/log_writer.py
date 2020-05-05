from influx_logging import InfluxHandler
import logging

influx_handler = InfluxHandler(database="error_log")
logging.getLogger().setLevel(logging.DEBUG)

influx_logger = logging.getLogger('influx_logging.tests.simple_message')
influx_logger.addHandler(influx_handler)
