from flask import *
import data_pipeline.daten_erheben.src.erhebung_historischer_daten.erhebung_historischer_daten as his
import data_pipeline.daten_erheben.src.erhebung_vorhersagedaten.erhebung_vorhersagedaten as forc
import data_pipeline.exception.exceptions as exc

app = Flask(__name__)


@app.route('/historische_datenerhebung', methods = ['POST'])
def get_historic_data():

    '''
    Name in documentation: 'historische_daten_erheben()'
    Gets called once the historical weather data gets updated.
    Therefore the URL where the ZIP-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    :return: statuscode
    '''

    response = {}
    try:

        if int(request.headers.get('Content-Length')) == 0:
            raise exc.IncompleteConfigException('Config-JSON empty.', 900)

        try:
            json.load(['historischURL'])
        except:
            raise exc.IncompleteConfigException('Historisch-URL missing in Config-JSON.', 900)

        url_historisch = request.get_json()['historischURL']

        his.raise_historic_data(url_historisch)

        response['statuscode'] = 200

    except exc.UrlException as uexc:
        response['statuscode'] = uexc.args[1]
    except exc.FileException as fexc:
        response['statuscode'] = fexc.args[1]
    except exc.RawDataException as rexc:
        response['statuscode'] = rexc.args[1]
    finally:
        return Response(status=response['statuscode'])


@app.route('/forecast_datenerhebung', methods = ['POST'])
def get_forecast_data():

    '''
    Name in documentation: 'vorhersagedaten_erheben()'
    Gets called once the forecast weather data gets updated.
    Therefore the URL where the KMZ-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    :return: statuscode
    '''

    response = {}
    try:

        if int(request.headers.get('Content-Length')) == 0:
            raise exc.IncompleteConfigException('Config-JSON empty.', 900)
        
        try:
            json.load(['forecastURL'])
        except:
            raise exc.IncompleteConfigException('Forecast-URL missing in Config-JSON.', 900)

        url_forecast = request.get_json()['forecastURL']

        forc.raise_forecast_data(url_forecast)

        response['statuscode'] = 200

    except exc.IncompleteConfigException as uexc:
        response['statuscode'] = uexc.args[1]
    except exc.UrlException as uexc:
        response['statuscode'] = uexc.args[1]
    except exc.FileException as fexc:
        response['statuscode'] = fexc.args[1]
    except exc.RawDataException as rexc:
        response['statuscode'] = rexc.args[1]
    finally:
        return Response(status=response['statuscode'])

if __name__ == '__main__':
    app.run(host='localhost', port='8000')