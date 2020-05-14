from flask import *
from data_pipeline.konfiguration.src.bereinigungs_config import bereinigungs_config as be_con
from data_pipeline.konfiguration.src.erhebungs_config import erhebungs_config as er_con
from data_pipeline.konfiguration.src.filterungs_config import filtern_config as fi_con
from data_pipeline.konfiguration.src.klassifikations_config import classification_config as kl_con
from data_pipeline.konfiguration.src.vorhersage_config import vorhersage_config as vs_con
from data_pipeline.konfiguration.src.frontend_interface_config import frontend_interface_config as fei_con

app = Flask(__name__)


@app.route('/erhebung_config', methods=['GET'])
def erhebung_config():
    """
    Name in documentation: erhebung_config()
    API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
    service Daten erheben.
    :return JSON-response with config.
    """
    return make_response(er_con)


@app.route('/bereinigung_config', methods=['GET'])
def bereinigung_config():
    """
   Name in documentation: bereinigung_config()
   API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
   service Daten bereinigen.
   :return JSON-response with config.
   """
    return make_response(be_con)


@app.route('/filterung_config', methods=['GET'])
def filterung_config():
    """
   Name in documentation: filterung_config()
   API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
   service Daten filtern.
   :return JSON-response with config.
   """
    return make_response(fi_con)


@app.route('/klassifikation_config', methods=['GET'])
def klassifikation_config():
    """
   Name in documentation: klassifikation_config()
   API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
   service Daten klassifizieren.
   :return JSON-response with config.
   """
    return make_response(kl_con)


@app.route('/vorhersage_config', methods=['GET'])
def vorhersage_config():
    """
   Name in documentation: vorhersage_config()
   API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
   service Vorhersage berechnen.
   :return JSON-response with config.
   """
    return make_response(vs_con)


@app.route('/frontend_interface_config', methods=['GET'])
def frontend_interface_config():
    """
   Name in documentation: frontend_interface_config()
   API callable via http-post-request when the pipeline-controller needs to access the config JSON-file for
   service Frontend-Interface.
   :return JSON-response with config.
   """
    return make_response(fei_con)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
