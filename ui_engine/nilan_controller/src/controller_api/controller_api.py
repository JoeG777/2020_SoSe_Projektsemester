from flask import *
import ui_engine.nilan_controller.src.data_pipeline_format_executor.data_pipeline_command_executor as dpce
import ui_engine.nilan_controller.src.modbus_command_executor.modbus_command_executor as mce
import data_pipeline.exception.exceptions as exc
import requests
import ui_engine.nilan_controller.src.controller_api.config as config

app = Flask(__name__)


@app.route('/')
def start():
    '''
    Name in documentation: ''
    triggers the index method
    :return: the link to index.html
    '''

    return redirect(url_for('index'))


@app.route('/index')
def index():
    '''
        Name in documentation: ''
        renders the index.html
        :return: index.html the site to be shown
    '''
    start_safari = "2020-01-05"
    end_safari = "2020-01-05"
    try:
        current_modbus = get_current_modbus()
    except Exception as e:
        return render_template('index.html',
                               value_start_safari=start_safari,
                               value_end_safari=end_safari,
                               value_raumtemperatur=21,
                               value_luefterstufe_zuluft=2,
                               value_luefterstufe_abluft=2,
                               value_betriebsmodus=0)


    vorhersage = 1
    raumtemperatur = current_modbus["temperatur"]["0"]
    luefterstufe_zuluft = current_modbus["zuluft_stufe"]["0"]
    luefterstufe_abluft = current_modbus["abluft_stufe"]["0"]
    betriebsmodus = current_modbus["modus"]["0"]
    return render_template('index.html',
                           value_start_safari=start_safari,
                           value_end_safari=end_safari,
                           #value_vorhersage=vorhersage,
                           value_raumtemperatur=raumtemperatur,
                           value_luefterstufe_zuluft=luefterstufe_zuluft,
                           value_luefterstufe_abluft=luefterstufe_abluft,
                           value_betriebsmodus=betriebsmodus)


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/validate_input', methods=['POST'])
def validate_input():
    '''
        Name in documentation: ''
        Validates from which button the input came and afterwards calls the right method.
        :return: index.html the site to be shown
    '''

    start_safari = None
    end_safari = None
    #vorhersage = None
    raumtemperatur = None
    luefterstufe_zuluft = None
    luefterstufe_abluft = None
    betriebsmodus = None

    try:

        start_safari = request.form['start_date']
        end_safari = request.form['end_date']
        #vorhersage = request.form.get('vorhersage')
        raumtemperatur = request.form['raumtemperaturSlider']
        luefterstufe_zuluft = request.form['lüfterZuluftSlider']
        luefterstufe_abluft = request.form['lüfterAbluftSlider']
        betriebsmodus = request.form['betriebsmodusSlider']

        if request.form['button'] == 'Vorhersage berechnen':
            exec_data_pipeline_cmd()

        else:
            exec_modbus_cmd()

        response = 200

    #except exc.DataPipelineException as dpxc:
    #    response = dpxc.args[1]
    #except exc.DBException as dbxc:
    #    response = dbxc.args[1]
    #except  exc.RawDataException as rdxc:
    #    response = rdxc.args[1]
    except Exception as exc:
        print("Error")
        start_safari = "18/03/1234 13:23"
        end_safari = "23/04/1456 14:23"
        raumtemperatur = 18
        luefterstufe_zuluft = 1
        luefterstufe_abluft = 1
        betriebsmodus = 1

    return render_template('index.html',
                           value_start_safari=start_safari,
                           value_end_safari=end_safari,
                           #value_vorhersage=vorhersage,
                           value_raumtemperatur=raumtemperatur,
                           value_luefterstufe_zuluft=luefterstufe_zuluft,
                           value_luefterstufe_abluft=luefterstufe_abluft,
                           value_betriebsmodus=betriebsmodus)

@app.route('/get_config')
def get_config():
    return json.dumps(config.config)

def exec_data_pipeline_cmd():
    '''
    Name in documentation: 'exec_data_pipeline_cmd'
    triggers the build_request_data_pipeline_cmd on data_pipeline_command_executer.
    '''
    print("Aktualisieren")
    dpce.build_request_data_pipeline_cmd(format_json())

def exec_modbus_cmd():
    '''
    Name in documentation: 'exec_modbus_cmd'
    triggers the build_request_modbus_cmd method on modbus_command_executer.
    '''
    print("Anwenden")
    mce.build_request_modbus_cmd(format_json())

def format_json():
    '''
    Requests the mandatory values from the index.html and saves it into a JSON-file.
    :return: json the formatted JSON-file
    '''
    json = {
        "start_datum": request.form['start_date'] + "T00:00:00Z",
        "end_datum": request.form['end_date'] + "T00:00:00Z",
        #"vorhersage": "1" if request.form.get('vorhersage') else "0",
        "raumtemperatur": round(int(request.form['raumtemperaturSlider']) / 100, 0),
        "luefterstufe_zuluft": round(int(request.form['lüfterZuluftSlider']), 0),
        "luefterstufe_abluft": round(int(request.form['lüfterAbluftSlider']), 0),
        "betriebsmodus": round(int(request.form['betriebsmodusSlider']) - 1, 0)
    }

    return json


def get_current_modbus():
    return mce.request_current_modbus()


@app.route('/get_model_data', methods=['GET'])
def get_current_models():
    return requests.get('http://localhost:5001/current_models').json()
