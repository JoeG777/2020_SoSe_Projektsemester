from flask import *
import data_pipeline.daten_erheben.get_historisch as his
import data_pipeline.daten_erheben.get_forecast as forc
import data_pipeline.daten_erheben.config as con

app = Flask(__name__)

@app.route('/')
def start():

    '''
    Forwards to the URL '/index' when the server gets called for the first time.
    '''

    return redirect(url_for('index'))

@app.route('/index')
def index():

    '''
    Opens 'index.html' to allow using the application.
    '''

    return render_template('index.html')

@app.route('/historischeDatenerhebung', methods = ['POST'])
def historische_datenerhebung():

    '''
    Gets called once the historical weather data gets updated.
    Therefore the URL where the ZIP-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    '''

    urlHistorisch = request.get_json()['historischURL']
    # urlHistorisch = con.configData["historischURL"]

    his.historische_daten_erheben(urlHistorisch)
    return render_template('index.html')

@app.route('/forecastDatenerhebung', methods = ['POST'])
def forecast_datenerhebung():

    '''
    Gets called once the forecast weather data gets updated.
    Therefore the URL where the KMZ-file gets pulled from is getting extracted from the parameters trough a request.
    Afterwards the method: 'historische_daten_erheben(url)' gets called and 'index.html' reopened.
    '''

    urlForecast = request.get_json()['forecastURL']

    # urlForecast = con.configData["forecastURL"]

    forc.vorhersage_daten_erheben(urlForecast)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port='8000')