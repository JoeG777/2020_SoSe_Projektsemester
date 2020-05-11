classification_config = {

    "datasource_raw_data": {'database': 'nilan_cleaned', 'measurement': 'temperature_register'},
    "datasource_enriched_data": {'database': 'nilan_enriched', 'measurement': 'training'},
    "datasource_marked_data": {'database': 'nilan_marked', 'measurement': 'training'},
    "datasource_classified_data": {'database': 'nilan_classified', 'measurement': 'classified'},
    "datasource_classifier": 'model.txt',
    "timeframe": ("2020-01-14 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"),
    "selected_event": "abtauzyklus",
    "new_classifier_method": "",
    "test_size": 0.3,
    "measurement": "temperature_register",
    "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.9, "offennutzung": 0.5, "luefterstufen": 0.8},
    "abtauzyklus": {'206', '205'},
    "warmwasseraufbereitung": {'210', '202'},
    # TODO : in ChangeLog eintragen
    "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                      "206": "evaporator"},
    "selected_event_options": {"abtauzyklus", "warmwasseraufbereitung", "ofennutzung", "luefterstufen"},
    "event_features": {
        "start_marker": 1.0,
        "start_deriv": 1.7,
        "start_evap": 1.0,
        "start_ch": -0.06,
        "start_abtau": 10.0,
        "end_marker": -1.0,
        "end_deriv": 0.5,
        "end_deriv_n3": -0.65,
        "end_shift": -1.0,
        "del_marker": 0.0,
    },
    "test_sample_size": 0.2,
    "classification_method": "kNN",
    "classification_method_options": {
        "SVM": "sklearn.svm.SVC()",
        "kNN": "sklearn.neighbors.KNeighborsClassifier()"
    }
}
