from unittest.mock import MagicMock
from flask import Response, jsonify


def test_delay_response_second_stroke_missing():
    import endpoint
    # Set up the global variables
    endpoint.first_stroke_result = (Response(), 200)
    endpoint.second_stroke_result = None
    # Mock the sleeper function
    mock_sleeper = MagicMock()
    # Call the function
    result = endpoint.delay_response(1, mock_sleeper)
    # Check that the sleeper was called with the correct arguments
    mock_sleeper.assert_called_once_with(1)
    # Check the result
    assert result == (jsonify({"message": "Second stroke not received"}), 200)
    # Check that the global variable was reset
    assert endpoint.first_stroke_result is None


def test_delay_response_second_stroke_received():
    import endpoint
    # Set up the global variables
    endpoint.first_stroke_result = (Response(), 200)
    endpoint.second_stroke_result = 'Y'
    # Mock the sleeper function
    mock_sleeper = MagicMock()
    # Call the function
    result = endpoint.delay_response(1, mock_sleeper)
    # Check that the sleeper was called with the correct arguments
    mock_sleeper.assert_called_once_with(1)
    # Check the result
    assert result is None
    # Check that the global variable was reset
    assert endpoint.second_stroke_result is None
