from flask import *
import data_pipeline.daten_erheben.get_historisch as his
import data_pipeline.daten_erheben.get_forecast as forc
import data_pipeline.daten_erheben.config as con

app = Flask(__name__)

@app.route('/')
def start():

    return redirect(url_for('index'))

@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/historischeDatenerhebung', methods = ['POST'])
def historische_datenerhebung():

    urlHistorisch = request.get_json()['historischURL']
    # urlHistorisch = con.configData["historischURL"]

    his.historische_daten_erheben(urlHistorisch)
    return render_template('index.html')

@app.route('/forcastDatenerhebung', methods = ['GET', 'POST'])
def forecast_datenerhebung():

    urlForecast = request.get_json()['forecastURL']
    timeOfSchedule = request.get_json()['timeOfSchedule']

    # urlForecast = con.configData["forecastURL"]

    forc.vorhersage_daten_erheben(urlForecast)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port='8000')