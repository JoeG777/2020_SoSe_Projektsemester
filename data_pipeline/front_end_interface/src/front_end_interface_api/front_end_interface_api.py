import flask
import front_end_interface.src.nilan_control_service as ncs
import front_end_interface.src.pipeline_control_service as pcs
import requests

app = Flask(__name__)

@app.route('/nilan_control_service')
def nilan_control_service():

    respone = None

    nilan_json = {
        "startdatum": requests.get('start_datum'),
        "enddatum": requests.get('end_datum'),
        "vorhersage": requests.get('vorhersage'),
        "raumtemperatur": requests.get('raumtemperatur'),
        "luefterstufe_zuluft": requests.get('luefterstufe_zuluft'),
        "luefterstufe_abluft": requests.get('luefterstufe_abluft'),
        "betriebsmodus": requests.get('betriebsmodus')
    }

    ncs.write_to_nilan(nilan_json)

    response = 200

@app.route('/pipeline_control_service')
def pipeline_control_service():

