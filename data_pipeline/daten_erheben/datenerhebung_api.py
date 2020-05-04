from flask import *
import data_pipeline.daten_erheben.get_historisch as his
import data_pipeline.daten_erheben.get_forecast as forc
import data_pipeline.daten_erheben.config as con

app = Flask(__name__)

@app.route('/')
def start():

    '''
    Leitet beim ersten Aufruf des Servers auf die URL /index weiter.
    '''

    return redirect(url_for('index'))

@app.route('/index')
def index():

    '''
    Öffnet die index.html zur Bedienung der Applikation.
    '''

    return render_template('index.html')

@app.route('/historischeDatenerhebung', methods = ['POST'])
def historische_datenerhebung():

    '''
    Wird aufgerufen, sobald die historischen Wetterdaten aktualisiert werden sollen.
    Dabei wird durch einen request aus den Parametern die URL zum Download der ZIP-Datei entnommen.
    Anschließend wird die Methode: 'historische_daten_erheben(url)' aufgerufen und erneut die index.html geöffnet.
    '''

    urlHistorisch = request.get_json()['historischURL']
    # urlHistorisch = con.configData["historischURL"]

    his.historische_daten_erheben(urlHistorisch)
    return render_template('index.html')

@app.route('/forecastDatenerhebung', methods = ['POST'])
def forecast_datenerhebung():

    '''
    Wird aufgerufen, sobald die Vorhersage-Wetterdaten aktualisiert werden sollen.
    Dabei wird durch einen request aus den Parametern die URL zum Download der KMZ-Datei entnommen.
    Anschließend wird die Methode: 'vorhersage_daten_erheben(url)' aufgerufen und erneut die index.html geöffnet.
    '''

    urlForecast = request.get_json()['forecastURL']

    # urlForecast = con.configData["forecastURL"]

    forc.vorhersage_daten_erheben(urlForecast)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port='8000')