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

    response = None
    try:

        if int(request.headers.get('Content-Length')) == 0:
            raise exc.IncompleteConfigException('Config-JSON empty.', 900)

        try:
            json.load(['historischURL'])
        except:
            raise exc.IncompleteConfigException('Historisch-URL missing in Config-JSON.', 900)

        url_historisch = request.get_json()['historischURL']

        his.raise_historic_data(url_historisch)

        response = 200

    except exc.UrlException as uexc:
        response = uexc.args[1]
    except exc.FileException as fexc:
        response = fexc.args[1]
    except exc.RawDataException as rexc:
        response = rexc.args[1]
    finally:
        return Response(status=response)


@app.route('/forecast_datenerhebung', methods = ['POST'])
def get_forecast_data():

    '''
    Name in documentation: 'vorhersagedaten_erheben()'
    Gets called once the forecast weather data gets updated.
    Therefore the URL where the KMZ-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    :return: statuscode
    '''

    response = None
    try:

        if int(request.headers.get('Content-Length')) == 0:
            raise exc.IncompleteConfigException('Config-JSON empty.', 900)
        
        try:
            json.load(['forecastURL'])
        except:
            raise exc.IncompleteConfigException('Forecast-URL missing in Config-JSON.', 900)

        url_forecast = request.get_json()['forecastURL']

        forc.raise_forecast_data(url_forecast)

        response = 200

    except exc.IncompleteConfigException as uexc:
        response = uexc.args[1]
    except exc.UrlException as uexc:
        response = uexc.args[1]
    except exc.FileException as fexc:
        response = fexc.args[1]
    except exc.RawDataException as rexc:
        response = rexc.args[1]
    finally:
        return Response(status=response)

if __name__ == '__main__':
    app.run(host='localhost', port='8000')