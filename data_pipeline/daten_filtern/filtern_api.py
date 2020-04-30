from flask import *
import filtern_config
import filtern_engine

app = Flask(__name__)

@app.route('/filtern' , methods = ['GET' , 'POST'])
def filtern():
    config = filtern_config

    filtern_engine.filtern(config)

    return render_template('index.html')