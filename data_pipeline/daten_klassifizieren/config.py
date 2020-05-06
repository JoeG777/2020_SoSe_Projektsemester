classification_config = {

    "datasource_raw_data": 'nilan',
    "datasource_training_data": 'database',
    "datasource_classified_data": 'classified_data',
    "datasource_classifier": 'model_np4.txt',
    "timeframe": ("2020-01-10 00:00:00", "2020-01-12 00:00:00"),
    "selected_event": "abtauzyklus",
    "new_classifier_method": "",
    "measurement": "temperature_register",
    "abtauzyklus": 206,
    # TODO : in ChangeLog eintragen
    "selected_event_options": {"Abtauzyklus","Warmwasseraufbereitung","Ofennutzung","Lüfterstufen"},
    "event_features" : {
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