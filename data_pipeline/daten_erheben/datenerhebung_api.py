from flask import *
import data_pipeline.daten_erheben.get_historisch as his
import get_forecast
import config
import influxdb_logging
import logging

app = Flask(__name__)

@app.route('/')
def start():

    return redirect(url_for('index'))

@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/historischeDatenerhebung', methods = ['GET', 'POST'])
def historische_datenerhebung():

    # urlHistorisch = request.json()['historischURL']

    urlHistorisch = config.configData["historischURL"]

    his.historische_daten_erheben(urlHistorisch)
    return render_template('index.html')

@app.route('/forcastDatenerhebung', methods = ['GET', 'POST'])
def forecast_datenerhebung():

    # urlForecast = request.json()['forecastURL']
    # timeOfSchedule = request.json()['timeOfSchedule']

    urlForecast = config.configData["forecastURL"]

    get_forecast.vorhersage_daten_erheben(urlForecast)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port='8000')
    influxdb_logging.InfluxHandler