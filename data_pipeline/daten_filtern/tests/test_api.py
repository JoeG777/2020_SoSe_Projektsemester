import unittest
import data_pipeline.daten_filtern.src.filtern_api.filtern_api as api
import requests
from mockito import *


class test_api(unittest.TestCase):

    url = "http://localhost:8000/filtern"

    config = {
        "variante": {
            "room": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "abtauzyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                }
            },
            "condenser": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "abtauzyklus": {
                    "delete": "True",
                    "Interpolation": "linear"
                }
            },
            "evaporator": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "abtauzyklus": {
                    "delete": "True",
                    "Interpolation": "linear"
                }
            },
            "inlet": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "abtauzyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                }
            },
            "outlet": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "abtauzyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                }
            },
            "freshAirIntake": {
                "WarmwWasserZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "OfenZyklus": {
                    "delete": "False",
                    "Interpolation": "linear"
                },
                "LüfterZyklus": {
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

    def test_response_200(self):

        request = requests.post(self.url, json = self.config)
        when2(api.filter).thenReturn(0)
        response = request.status_code
        self.assertEqual(response, 200)


if __name__ == "__main__":
    unittest.main()