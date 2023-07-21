from unittest.mock import patch
from unittest.mock import mock_open

import pytest
from flask import Response, jsonify, Flask
import endpoint


def test_delay_response_second_stroke_missing():
    # creates a Flask app and set up an application context
    app = Flask(__name__)
    with app.app_context():
        # sets up the global variables
        endpoint.first_stroke_result = (Response(), 200)
        endpoint.second_stroke_result = None
        # calls the function
        result = endpoint.delay_response(1)
        # checks the result
        assert result[0].get_json() == jsonify({"message": "Second stroke not received"}).get_json() \
               and result[1] == 200
        # checks that the global variable was reset
        assert endpoint.first_stroke_result is None


def test_delay_response_second_stroke_received():
    # creates a Flask app and set up an application context
    app = Flask(__name__)
    with app.app_context():
        # sets up the global variables
        endpoint.first_stroke_result = (Response(), 200)
        endpoint.second_stroke_result = 'Y'
        # calls the function
        result = endpoint.delay_response(1)
        # checks the result
        assert result is None
        # checks that the global variable was reset
        assert endpoint.second_stroke_result is None


# patch decorator replaces real objects in code with mock instances for test
@patch('json.dump')
@patch('builtins.open', new_callable=mock_open)
def test_receive_json(mocked_open_param, mock_dump_param):
    # creates a Flask app and set up an application and request context
    app = Flask(__name__)
    with app.app_context(), \
            app.test_request_context(), \
            patch("endpoint.request") as mock_request, \
            patch("endpoint.recogniser_function") as mock_recogniser:
        # setup mock values
        mock_request.headers.get.return_value = 'RR'
        mock_request.get_json.return_value = {'data': 'sample data'}
        mock_recogniser.return_value = (jsonify({"message": "Sign RR correct"}), 200)

        # calls function for the first stroke
        result = endpoint.receive_json()

        # verifies results of second stroke
        assert result[0].get_json() == jsonify({"message": "Sign RR correct"}).get_json()
        assert result[1] == 200


if __name__ == '__main__':
    pytest.main()
