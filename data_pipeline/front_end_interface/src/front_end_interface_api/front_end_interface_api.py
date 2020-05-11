import flask
import front_end_interface.src.nilan_control_service as ncs
import front_end_interface.src.pipeline_control_service as pcs

app = Flask(__name__)

@app.route('/nilan_control_service')
def nilan_control_service():

    ncs.write_to_nilan()

@app.route('/pipeline_control_service')
def pipeline_control_service():

