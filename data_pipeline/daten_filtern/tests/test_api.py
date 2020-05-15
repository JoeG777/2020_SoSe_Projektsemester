import unittest
import data_pipeline.daten_filtern.src.filtern_api.filtern_api as api
import requests
from mockito import *


class test_api(unittest.TestCase):

    url = "http://localhost:8000/filtern"

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
        request = requests.post(self.url, json = config)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)


    def test_response_900_config_error(self):
        config_wrong_curvename = {
            "filtern_config": {
                "timeframe": ["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
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
        request = requests.post(self.url, json = config_wrong_curvename)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

if __name__ == "__main__":
    unittest.main()