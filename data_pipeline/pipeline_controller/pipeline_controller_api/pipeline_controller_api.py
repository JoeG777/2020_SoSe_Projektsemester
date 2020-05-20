from data_pipeline.pipeline_controller.process_engine import process_engine
from data_pipeline.log_writer.log_writer import Logger
from data_pipeline.pipeline_controller.request_service import request_service

LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "uipserver.ddns.net"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Vorhersage berechnen"

logger = Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT,
                LOGGER_COMPONENT)

from flask import *
from data_pipeline.pipeline_controller.config_handler import config_handler

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
    process_engine.start_trigger_based_process()
    return "Success!"


@app.route('/config', methods=['POST'])
def config():
    logger.info("incoming request for config")
    json = request.get_json()
    return config_handler.fetch_config(json["config"]).json()


@app.route('/classfiy', methods=['POST'])
def classify():
    logger.info("incoming request for classification")
    json = request.get_json()
    request_service.start_classification(json)
    return "Success!"
