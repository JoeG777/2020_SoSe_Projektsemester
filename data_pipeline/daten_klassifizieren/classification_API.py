from flask import *
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import data_pipeline.daten_klassifizieren.classification_engine as classification
import data_pipeline.daten_klassifizieren.training_engine as training

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():


@app.route('/train', methods=['POST'])
def train():


#if __name__ == '__main__':
#  app.run(host='127.0.0.1', port=5000)
