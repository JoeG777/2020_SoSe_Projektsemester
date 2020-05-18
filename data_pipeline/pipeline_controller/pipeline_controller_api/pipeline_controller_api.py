from data_pipeline.pipeline_controller.process_engine import process_engine
from data_pipeline.log_writer.log_writer import Logger
LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "uipserver.ddns.net"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Vorhersage berechnen"

logger = Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT,
                LOGGER_COMPONENT)

from flask import *

app = Flask(__name__)

http_status_codes = {
    "HTTPBadRequest": 400,
    "HTTPInternalServerError": 500,
    "ConfigException": 900,
    "DBException": 901,
    "PersistorException": 902
}

if __name__ == '__main__':
    app.run(host='localhost', port=5000)


@app.route('/start_process', methods=['POST'])
def start_process():
    logger.info("lets gooo")
    return process_engine.start_timer_based_process_cycle()
