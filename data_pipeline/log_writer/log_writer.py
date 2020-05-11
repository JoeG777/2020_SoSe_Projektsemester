from influx_logging import InfluxHandler
import logging

class Logger():

    dic = {"host": "uipserver.ddns.net",
           "port": 8086,
           "username": "student",
           "password": "Abtauzyklus"
    }
    def __init__(self):

        self.influx_handler = InfluxHandler(database="logs", measurement="logs", **Logger.dic)
        logging.getLogger().setLevel(logging.DEBUG)

        self.influx_logger = logging.getLogger('influx_logging.tests.simple_message')
        self.influx_logger.addHandler(self.influx_handler)



