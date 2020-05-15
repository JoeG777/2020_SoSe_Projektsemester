from timeloop import Timeloop
from datetime import timedelta
from data_pipeline.pipeline_controller.config_handler.config_handler import fetch_all_configs, fetch_config
from data_pipeline.pipeline_controller.request_service.request_service import start_historic_data_elicitation, \
    start_prediction_data_elicitation, start_cleaning, start_classification, start_classification_training, \
    start_filtering, start_prediction_training, drop_get_request, start_prediction

tl = Timeloop()


@tl.job(interval=timedelta(hours=24))
def start_timer_based_process_cycle():
    tl.start(block=True)
    all_configs = fetch_all_configs()
    start_historic_data_elicitation(all_configs["elicitation"])
    start_prediction_data_elicitation(all_configs["elicitation"])
    start_cleaning(all_configs["cleaning"])
    start_classification(all_configs["classification"])
    start_classification_training(all_configs["classification"])
    start_filtering(all_configs["filtering"])
    start_prediction_training(all_configs["prediction"])


def start_trigger_based_process():
    config = fetch_config("prediction")
    start_prediction(config)
