from unittest import TestCase
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_api.prediction_api as pred_api

class test_train(TestCase):

    def test_invalid_config_should_return_400(self):
        self.app = pred_api.app.test_client()
        response = self.app.post('/train')
        assert '400' in str(response.status_code)
