from flask import *
import data_pipeline.daten_erheben.src.historic_data.get_historisch as his
import data_pipeline.daten_erheben.src.forecast_data.get_forecast as forc
import data_pipeline.daten_erheben.src.exception as exc

app = Flask(__name__)


@app.route('/')
def start():

    '''
    Forwards to the URL '/index' when the server gets called for the first time.
    :return: Redirects to '/index'
    '''

    return redirect(url_for('index'))


@app.route('/index')
def index():

    '''
    Opens 'index.html' to allow using the application.
    :return: Opens 'index.html'
    '''

    return render_template('index.html')


@app.route('/historischeDatenerhebung', methods = ['POST'])
def historische_datenerhebung():

    '''
    Gets called once the historical weather data gets updated.
    Therefore the URL where the ZIP-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    :return: Opens 'index.html'
    '''

    response = {}
    try:
        urlHistorisch = request.get_json()['historischURL']
        if not urlHistorisch:
            raise exc.UrlException("URL incorrect", 904)
        his.historische_daten_erheben(urlHistorisch)
    except exc.UrlException as uexc:
        response['statuscode'] = uexc.args[1]
    except exc.FileException as fexc:
        response['statuscode'] = fexc.args[1]
    except exc.RawDataException as rexc:
        response['statuscode'] = rexc.args[1]
    finally:
        return make_response(jsonify({'statuscode': response['statuscode']}))


@app.route('/forecastDatenerhebung', methods = ['POST'])
def forecast_datenerhebung():

    '''
    Gets called once the forecast weather data gets updated.
    Therefore the URL where the KMZ-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    :return: Opens 'index.html'
    '''

    response = {}
    try:
        urlForecast = request.get_json()['forecastURL']
        if not urlForecast:
            raise exc.UrlException("URL incorrect", 904)
        forc.vorhersage_daten_erheben(urlForecast)
    except exc.UrlException as uexc:
        response['statuscode'] = uexc.args[1]
    except exc.FileException as fexc:
        response['statuscode'] = fexc.args[1]
    except exc.RawDataException as rexc:
        response['statuscode'] = rexc.args[1]
    finally:
        return make_response(jsonify({'statuscode': response['statuscode']}))

if __name__ == '__main__':
    app.run(host='localhost', port='8000')