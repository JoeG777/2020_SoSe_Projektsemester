import data_pipeline.db_connector.src.read_manager.read_manager as rm

default_measurement = "measurement"

register_dict = {
    "Fresh Air Intake": "201",
    "Inlet": "202",
    "Room": "210",
    "Outlet": "204",
    "Condenser": "205",
    "Evaporator": "206"
}


def train(config):
    all_models = []
    for prediction_unit in config:
        all_models.append(train_model(prediction_unit))
        get_data()


def save_prediction_model(all_models, config):
    return ""


def train_model(prediction_unit):
    return ""


def get_data(register):
    print("getting data")
    return rm.read_register_of_measurement("temperature_register", register_dict[register])

def get_all_data():
    keys = register_dict.keys()
    data = []
    for key in keys:





def calculate_average_score():
    return " "

print(get_data("Fresh Air Intake"))