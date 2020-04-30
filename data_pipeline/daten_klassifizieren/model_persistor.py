from sklearn import svm
import pickle
#import logWriter
import pandas as pd

classification_config = {

    "datasource_raw_data" : ("host", "port", "username", "database", "password"),
    "datesource_training_data" : ("host", "port", "username", "database", "password"),
    "datasource_classified_data" : ("host", "port", "username", "database", "password"),
    "timeframe" :("2020-01-05 00:00", "2020-02-05 00:00"),
    "selected_event" :"Abtauzyklus",
    "event_features" : {
        "Ableitung_start": 1.0,
        "Ableitung_ende": -1.0
    },
    "test_sample_size" : 0.2,
    "classification_method_options" : {
        "SVM" : "model = SVM()",
        "kNN" : "model = KNeighbors()"
    }
}

def load_classifier(config):
    serialized_model = pickle.load(open("model.txt", "rb"))

def persist_classifier():

    classification_model = svm.SVC()
    serialized_model = pickle.dump(classification_model, open("model.txt", "wb"))
    print(serialized_model)
    return 0

persist_classifier()