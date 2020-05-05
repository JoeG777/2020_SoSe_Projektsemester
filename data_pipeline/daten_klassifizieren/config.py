classification_config = {

    "datasource_raw_data" : (host, port, username, database, password),
    "datasource_training_data" : (host, port, username, database, password),
    "datasource_classified_data" : (host, port, username, database, password),
    "timeframe" :("2020-01-05 00:00", "2020-02-05 00:00"),
    "selected_event" :"Abtauzyklus",
    "new_classifier_method": "kNN",
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
    "classification_method" : "SVM",
    "classification_method_options" : {
        "SVM" : "model = SVM()",
        "kNN" : "model = KNeighbors()"
    }
}