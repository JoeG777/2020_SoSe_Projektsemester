import unittest
from sklearn import neighbors
from mockito.matchers import ANY
from mockito import *
import data_pipeline.log_writer.log_writer as logger
when(logger).Logger(ANY, ANY, ANY, ANY, ANY).thenReturn \
    (mock(dict(info=lambda x: print(x), warning=lambda x: print(x),
               error=lambda x: print(x), write_into_measurement=lambda x: print(x))))

import data_pipeline.daten_klassifizieren.training_engine as training


class TestEvaluateClassifier(unittest.TestCase):
    model = neighbors.KNeighborsClassifier()

    @classmethod
    def setUp(self):
        unstub()

    def test_classifier_is_better_than_required_score(self):
        when2(self.model.score, ANY, ANY).thenReturn(0.9)
        self.assertEqual(training.evaluate_classifier(self.model, 0.8, ANY, ANY), True)

    def test_classifier_is_worse_than_required_score(self):
        when2(self.model.score, ANY, ANY).thenReturn(0.8)
        self.assertEqual(training.evaluate_classifier(self.model, 0.9, ANY, ANY), False)


if __name__ == '__main__':
    unittest.main()
