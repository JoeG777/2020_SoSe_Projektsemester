from unittest import TestCase
from data_pipeline.vorhersage_berechnen.src.prediction_core.config_validator.config_validator import validate_config
from data_pipeline.exception.exceptions import *


class test_validate_config(TestCase):

    def test_config_is_valid_should_return_void(self):
        valid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
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
                        "independent": ["freshAirIntake", "condenser"],
                        "dependent": ["room"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["condenser"],
                        "dependent": ["evaporator", "outlet"],
                        "test_sample_size": 0.2
                    },
                ],
                "anotherOption": [
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
                        "independent": ["freshAirIntake", "condenser"],
                        "dependent": ["room"],
                        "test_sample_size": 0.2
                    },
                    {
                        "independent": ["condenser"],
                        "dependent": ["evaporator", "outlet"],
                        "test_sample_size": 0.2
                    },
                ]
            },
        }

        validate_config(valid_config)

    def test_config_is_of_wrong_type(self):
        invalid_config_one = None
        invalid_config_two = 2

        self.assertRaises(ConfigTypeException, validate_config, invalid_config_one)
        self.assertRaises(ConfigException, validate_config, invalid_config_two)

    def test_config_misses_selected_value_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options" : {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 0.2
                    }]
            }
        }

        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_misses_database_options_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_database_options_has_invalid_key_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_database_options_misses_prediction_key_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_database_options_is_not_of_type_dict_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": None,
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_database_options_training_is_not_of_type_dict_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": None,
                "prediction": {
                    "datasource_forecast_dbname": "111", # this is wrong
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_database_options_prediction_is_not_of_type_dict_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": None
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_database_options_training_misses_mandatory_key_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": {
                    "aaa": "yalla", # this is wrong
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }

        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_database_options_training_has_invalid_value_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": {
                    "datasource_forecast_dbname": 1, # this is wrong
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_misses_prediction_options_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            }
        }

        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_prediction_options_is_not_a_dict_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": None,
        }
        
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_configs_selected_value_is_not_of_type_str_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"
                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": None
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_selected_prediction_option_contains_invalid_list_item_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    None
                ]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_configs_training_percentage_is_not_number_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 'Not of type number'
                    }]
            }
        }
        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_configs_dependent_is_not_a_list_should_raise_InvalidConfigValueException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": None,
                        "test_sample_size": 1
                    }]
            }
        }

        self.assertRaises(InvalidConfigValueException, validate_config, invalid_config)

    def test_config_misses_dependent_key_should_raise_InvalidConfigKeyException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "test_sample_size": 0.2
                    }]
            }
        }

        self.assertRaises(InvalidConfigKeyException, validate_config, invalid_config)

    def test_config_is_incomplete_should_raise_IncompleteConfigException(self):
        # see check_completeness
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "room", "inlet", "condenser"],
                        "test_sample_size": 1
                    }]
            }
        }
        self.assertRaises(IncompleteConfigException, validate_config, invalid_config)

    def test_config_has_redundant_curves(self):
        # see check_redundancies
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1
                    },
                    {
                        "independent": ["room"],
                        "dependent": ["evaporator"],
                        "test_sample_size": 1
                    }],
            }
        }
        self.assertRaises(RedundantConfigException, validate_config, invalid_config)

    def test_config_has_same_curve_as_dependent_twice_should_raise_RedundantConfigException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor", "outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1
                    }]
            }
        }
        self.assertRaises(RedundantConfigException, validate_config, invalid_config)

    def test_config_has_same_curve_as_independent_twice_should_raise_RedundantConfigException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "room", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1
                    }]
            }
        }
        self.assertRaises(RedundantConfigException, validate_config, invalid_config)

    def test_config_has_invalid_prediction_chain_should_raise_InconsistentConfigException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "inlet"],
                        "test_sample_size": 1
                    },
                    {
                        "independent": ["condenser"],
                        "dependent": ["condenser"],
                        "test_sample_size": 1
                    },
                    {
                        "independent": ["outlet"],
                        "dependent": ["room"],
                        "test_sample_size": 1
                    },
                ]
            }
        }

        self.assertRaises(InconsistentConfigException, validate_config, invalid_config)

    def test_config_contains_training_percentage_below_one_should_raise_InvalidTrainingPercentageException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": -1
                    }]
            }
        }

        self.assertRaises(InvalidTrainingPercentageException, validate_config, invalid_config)

    def test_config_contains_training_percentage_above_one_should_raise_InvalidTrainingPercentageException(self):
        invalid_config = {
            "selected_value": "default",
            "database_options": {
                "training": {
                    "datasource_nilan_dbname": "name",
                    "datasource_nilan_measurement": "name",
                    "datasource_weatherdata_dbname": "name",
                    "datasource_weatherdata_measurement": "name"


                },
                "prediction": {
                    "datasource_forecast_dbname": "yalla",
                    "datasource_forecast_measurement": "name",
                    "datasource_forecast_register": "name",
                    "datasink_prediction_dbname": "name",
                    "datasink_prediction_measurement": "name"
                }
            },
            "prediction_options": {
                "default": [
                    {
                        "independent": ["outdoor"],
                        "dependent": ["evaporator", "outlet", "freshAirIntake", "room", "inlet", "condenser"],
                        "test_sample_size": 1.1
                    }]
            }
        }

        self.assertRaises(InvalidTrainingPercentageException, validate_config, invalid_config)



