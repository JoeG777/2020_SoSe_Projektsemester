import unittest
import data_pipeline.daten_filtern.src.filtern_api.filtern_api as api
import requests
from mockito import *


class test_api(unittest.TestCase):

    url = "http://localhost:8000/filtern"

    config = {
        "filtern_config": {
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

    config_wrong_curvename = {
        "filtern_config": {
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

    config_curve_missing = {
        "filtern_config": {
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
    config_wrong_cyclename = {
        "filtern_config": {
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
    config_cycle_missing = {
        "filtern_config": {
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
    config_delete_wrong= {
        "filtern_config": {
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
    config_delete_missing = {
        "filtern_config": {
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
    congig_interpolation_wrong= {
        "filtern_config": {
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

    config_interpolation_missing = {
        "filtern_config": {
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



    def test_response_200(self):

        request = requests.post(self.url, json = self.config)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)

    def test_response_900_config_error_curve_wrong(self):

        request = requests.post(self.url, json = self.config_wrong_curvename)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_curve_missing(self):

        request = requests.post(self.url, json = self.config_curve_missing)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_cycle_wrong(self):

        request = requests.post(self.url, json = self.config_wrong_cyclename)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_cycle_missing(self):

        request = requests.post(self.url, json = self.config_cycle_missing)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_delete_named_wrong(self):

        request = requests.post(self.url, json = self.config_delete_wrong)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_delete_missing(self):

        request = requests.post(self.url, json = self.config_delete_missing)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_interpolation_named_wrong(self):

        request = requests.post(self.url, json = self.congig_interpolation_wrong)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)

    def test_response_900_config_error_interpolation_missing(self):

        request = requests.post(self.url, json = self.config_interpolation_missing)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 900)


if __name__ == "__main__":
    unittest.main()