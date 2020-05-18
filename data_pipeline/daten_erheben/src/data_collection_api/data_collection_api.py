from flask import *
import data_pipeline.daten_erheben.src.erhebung_historischer_daten.erhebung_historischer_daten as his
import data_pipeline.daten_erheben.src.erhebung_vorhersagedaten.erhebung_vorhersagedaten as forc
import data_pipeline.exception.exceptions as exc
import data_pipeline.log_writer.log_writer as logger

app = Flask(__name__)
logger = logger.Logger("logs", "logs", "uipserver.ddns.net", 8086,"Datenerhebung")


@app.route('/historische_datenerhebung', methods=['POST'])
def get_historic_data():
    '''
    Name in documentation: 'historische_daten_erheben'
    Gets called once the historical weather data gets updated.
    Therefore the URL where the ZIP-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called.
    :return: statuscode
    '''

    response = None
    try:

        json_validation('historischURL')

        url_historisch = request.get_json(force=True)['historischURL']

        his.raise_historic_data(url_historisch)

        response = 200

    except exc.DataPipelineException as dpxc:
        response = dpxc.args[1]
    except exc.IncompleteConfigException as icxc:
        response = icxc.args[1]
    finally:
        return Response(status=response)


@app.route('/forecast_datenerhebung', methods=['POST'])
def get_forecast_data():
    '''
    Name in documentation: 'vorhersagedaten_erheben'
    Gets called once the forecast weather data gets updated.
    Therefore the URL where the KMZ-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called.
    :return: statuscode
    '''

    response = None
    try:

        json_validation('forecastURL')

        url_forecast = request.get_json(force=True)['forecastURL']

        forc.raise_forecast_data(url_forecast)

        response = 200

    except exc.DataPipelineException as dpxc:
        response = dpxc.args[1]
    except exc.IncompleteConfigException as icxc:
        response = icxc.args[1]
    finally:
        return Response(status=response)


def json_validation(index):
    '''
    Name in documentation: 'json_validation'
    Gets called in the beginning of either 'get_forecast_data' or 'get_historic_data' to proof wether the passed config data
    is complete or not.
    :param index: Depending on the passed index, the config gets checked for another tag. Either 'forecastURL' or 'historischURL'.
    '''

    if int(request.headers.get('Content-Length')) == 0:
        logger.info('Config-JSON empty')
        raise exc.IncompleteConfigException('Config-JSON empty.', 900)

    try:
        request.get_json(force=True)[index]
    except:
        logger.info(index + 'missing in Config-JSON')
        raise exc.IncompleteConfigException(index + 'missing in Config-JSON.', 900)


if __name__ == '__main__':
    app.run(host='localhost', port='8000')
