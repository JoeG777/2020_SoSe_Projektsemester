classification_config = {

    "datasource_raw_data": 'nilan',
    "datasource_training_data": 'database',
    "datasource_classified_data": 'classified_data',
    "timeframe":("2020-01-05 00:00:00", "2020-01-09 00:00:00"),
    "selected_event": "abtauzyklus",
    "new_classifier_method": "kNN",
    "measurement": "temperature_register",
    "abtauzyklus": 206,
    # TODO : in ChangeLog eintragen
    "selected_event_options": {"Abtauzyklus","Warmwasseraufbereitung","Ofennutzung","Lüfterstufen"},
    "event_features" : {
        "start_marker": 1.0,
        "start_deriv": 1.0,
        "start_evap": 0.0,
        "start_ch": -0.06,
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