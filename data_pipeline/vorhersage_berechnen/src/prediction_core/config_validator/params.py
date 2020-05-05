prediction_config = {
    "selected_value" : "default",
    "prediction_options" : {
        "default": [
            {
                "independent": ["outdoor"],
                "dependent": ["freshAirIntake"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["freshAirIntake"],
                "dependent": ["condenser"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["freshAirIntake"],
                "dependent": ["inlet"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["freshAirIntake", "condenser", "evaporator"],
                "dependent": ["room"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["freshAirIntake", "condenser"],
                "dependent": ["evaporator"],
                "test_sample_size": 0.2
            },
            {
                "independent": ["freshAirIntake"],
                "dependent": ["outlet"],
                "test_sample_size": 0.2
            }
        ]
        },

        "option1" : [
            {
                "type": "standard",
                "independent": ["outdoor"],
                "dependent": ["freshArIntake"],
                "test_sample_size": 0.2
            },
            {
                "type": "standard",
                "independent": ["freshArIntake"],
                "dependent": ["condenser"],
                "test_sample_size": 0.2
            },
            {
                "type": "standard",
                "independent": ["freshArIntake"],
                "dependent": ["inlet"],
                "test_sample_size": 0.2
            },
            {
                "type": "multi",
                "independent": ["freshArIntake", "condenser", "evaporator"],
                "dependent": ["room"],
                "test_sample_size": 0.2
            },
            {
                "type": "multi",
                "independent": ["freshArIntake", "condenser"],
                "dependent": ["evaporator"],
                "test_sample_size": 0.2
            },
            {
                "type": "standard",
                "independent": ["freshArIntake"],
                "dependent": ["outlet"],
                "test_sample_size": 0.2
            }
        ],
    }



