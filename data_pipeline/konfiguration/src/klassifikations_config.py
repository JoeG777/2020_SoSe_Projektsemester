classification_config = {
    "datasource_classifier": "model.txt",
    "required_score": {"abtauzyklus": 0.9, "warmwasseraufbereitung": 0.9, "offennutzung": 0.5, "luefterstufen": 0.8},
    "abtauzyklus": ["206", "205"],
    "warmwasseraufbereitung": ["210", "202"],
    "register_dict": {"201": "freshAirIntake", "202": "inlet", "210": "room", "204": "outlet", "205": "condenser",
                      "206": "evaporator"},
    "selected_event_options": ["abtauzyklus", "warmwasseraufbereitung", "ofennutzung", "luefterstufen"],
    "datasource_raw_data": {"database": "bereinigte_Daten", "measurement": "temperature"},
    "datasource_enriched_data": {"database": "nilan_enriched", "measurement": "training"},
    "datasource_marked_data": {"database": "nilan_marked", "measurement": "training"},
    "datasource_classified_data": {"database": "nilan_classified", "measurement": "classified"},
    "timeframe": ["2020-01-12 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
    "selected_event": "abtauzyklus",
    "create_new_classifier": "",
    "test_size": 0.3,
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
        "del_marker": 0.0
    }
}
