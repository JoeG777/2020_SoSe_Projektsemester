import unittest
import requests


class test_train(unittest.TestCase):

    def test_response_200(self):
        request = requests.post('http://127.0.0.1:5000/train', json={"Hallo": "ich bin ein Request"})
        response = request.status_code
        self.assertEqual(response, 200)

    def test_invalid_config(self):
        request = requests.post('http://127.0.0.1:5000/train', json="Hallo")
        response = request.status_code
        self.assertEqual(response, 500)


if __name__ == '__main__':
    unittest.main()
