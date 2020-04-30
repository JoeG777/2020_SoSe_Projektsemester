from flask import *
from filtern_config import filtern_config
import filtern_engine

app = Flask(__name__)

@app.route('/filtern' , methods = ['GET' , 'POST'])
def filtern():
    config = filtern_config["filter_options"][filtern_config["selected_value"]]

    filtern_engine.filtern(config)

    return render_template('index.html')