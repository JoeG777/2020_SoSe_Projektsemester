classification_config = {

    "datasource_raw_data": {'database': 'nilan', 'measurement': 'temperature_register'},
    "datasource_training_data": {'database': 'nilan_erweitert', 'measurement': 'training'},
    "datasource_classified_data": 'classified_data',
    "datasource_classifier": 'model.txt',
    "timeframe": ("2020-01-10 00:00:00", "2020-01-12 00:00:00"),
    "selected_event": "abtauzyklus",
    "new_classifier_method": "kNN",
    "test_size": 0.3,
    "measurement": "temperature_register",
    "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.9, "offennutzung": 0.5, "luefterstufen": 0.8},
    "abtauzyklus": 206,
    # TODO : in ChangeLog eintragen
    "selected_event_options": {"abtauzyklus", "warmwasseraufbereitung", "ofennutzung", "luefterstufen"},
    "event_features": {
        "start_marker": 1.0,
        "start_deriv": 1.0,
        "start_evap": 0.0,
        "start_ch": -0.06,
        "start_abtau": 10.0,
        "end_marker": -1.0,
        "end_deriv": 0.5,
        "end_shift": -1.0,
        "del_marker": 0.0
    },
    "test_sample_size" : 0.2,
    "classification_method" : "kNN",
    "classification_method_options" : {
        "SVM": "sklearn.svm.SVC()",
        "kNN": "sklearn.neighbors.KNeighborsClassifier()"
    }
}