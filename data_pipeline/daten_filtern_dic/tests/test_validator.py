import unittest
from data_pipeline.daten_filtern_dic.src.filtern_validator import filtern_validator
from data_pipeline.exception import exceptions as exe

class test_validator(unittest.TestCase):

    def test_response_200(self):
        config = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        filtern_validator.config_validation(config["filtern_config"])

    def test_response_900_config_error_curve_wrong(self):
        config_wrong_curvename = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "!!room!!": { #Wrong Curve Name
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_wrong_curvename["filtern_config"])

    def test_response_900_config_error_curve_missing(self):
        config_curve_missing = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        #room missing
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_curve_missing["filtern_config"])

    def test_response_900_config_error_curve_missing(self):
        config_wrong_cyclename = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "!!!warmwasseraufbereitung!!!": { #warmwasseraufbereitung named wrong
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_wrong_cyclename["filtern_config"])

    def test_response_900_config_error_cycle_missing(self):
        config_cycle_missing = {
        "filtern_config": {
            "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
            "selected_value": "variante",
            "filter_options": {
                "default": {
                    "room": {
                        "warmwasseraufbereitung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "condenser": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "evaporator": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "inlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "outlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "freshAirIntake": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    }
                },
                "variante": {
                    "room": {
                        #warmwasseraufbereitung missing
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "condenser": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "evaporator": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "inlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "outlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "freshAirIntake": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    }
                }
            }
        }
    }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_cycle_missing["filtern_config"])

    def test_response_900_config_error_delete_named_wrong(self):
        config_delete_wrong= {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "!!!False!!!", #delete named wrong
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_delete_wrong["filtern_config"])

    def test_response_900_config_error_delete_missing(self):
        config_delete_missing = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "warmwasseraufbereitung": {
                                #Delete missing
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_delete_missing["filtern_config"])

    def test_response_900_config_error_interpolation_named_wrong(self):
        congig_interpolation_wrong= {
        "filtern_config": {
            "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
            "selected_value": "variante",
            "filter_options": {
                "default": {
                    "room": {
                        "warmwasseraufbereitung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "condenser": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "evaporator": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "inlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "outlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "freshAirIntake": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "True",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    }
                },
                "variante": {
                    "room": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "!!!linear!!!" #Interpolation named wrong
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "condenser": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "evaporator": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "True",
                            "Interpolation": "linear"
                        }
                    },
                    "inlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "outlet": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    },
                    "freshAirIntake": {
                        "warmwasseraufbereitung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "ofennutzung": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "luefterstufen": {
                            "delete": "False",
                            "Interpolation": "linear"
                        },
                        "abtauzyklus": {
                            "delete": "False",
                            "Interpolation": "linear"
                        }
                    }
                }
            }
        }
    }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(congig_interpolation_wrong["filtern_config"])

    def test_response_900_config_error_interpolation_missing(self):
        config_interpolation_missing = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "False"
                                #Interpolation missing
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_interpolation_missing["filtern_config"])

    def test_response_900_config_empty(self):
        config_empty = {}
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_empty)

    def test_respone_900_config_wrong_timefromat(self):
        config_timeframe_wrong = {
            "filtern_config": {
                "timeframe": ["Missing", "2020-01-20 12:00:00.000 UTC"],
                "selected_value": "variante",
                "filter_options": {
                    "default": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "True",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    },
                    "variante": {
                        "room": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "condenser": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "evaporator": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "True",
                                "Interpolation": "linear"
                            }
                        },
                        "inlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "outlet": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        },
                        "freshAirIntake": {
                            "warmwasseraufbereitung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "ofennutzung": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "luefterstufen": {
                                "delete": "False",
                                "Interpolation": "linear"
                            },
                            "abtauzyklus": {
                                "delete": "False",
                                "Interpolation": "linear"
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(exe.ConfigException):
            filtern_validator.config_validation(config_timeframe_wrong)

if __name__ == '__main__':
    unittest.main()
