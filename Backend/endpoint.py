from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from extraction import *
from sign_a import is_sign_a
from sign_b import is_sign_b
import string

# Creates basic flask application
app = Flask(__name__)
# Cross-Origin Resource Sharing enabled for all routes
CORS(app)


# Creates endpoint that listens for POST requests
@app.route('/receive_json', methods=['POST'])
def receive_json() -> Tuple[Response, int]:
    """
        Receives message from frontend with sign in header and touch data as JSON file.
        :rtype: tuple where first object is flask jsonify response object, second is HTTP status code
        :return: two objects: first object is flask jsonify response object, second is HTTP status code
    """
    # gets header/indicator for sign
    sign: string = request.headers.get('Sign')
    # gets JSON file
    data: Union[List[Dict[str, Union[float, List[float]]]], None] = request.get_json()
    # for parametrisation purposes
    print(sign)
    print(data)
    # if data is none, returns error message
    if not data:
        print("not data")
        return jsonify({"message": "No JSON received"}), 400

    # gives json into recogniser
    response: Tuple[Response, int] = recogniser_function(sign, data)

    # returns Response (imported from Flask) and HTTP status code
    return response


# finish and write docstring
def recogniser_function(sign: string, data: List[Dict[str, Union[float, List[float]]]]) -> Tuple[Response, int]:
    """
        Extracts timestamps and locations into two individual arrays, and feeds it into respective recognisers,
        depending on the sign.
        :rtype: tuple
        :param sign: the sign that is being passed into the function, represented by a string
        :param data: the touch data detected by the touch screen, in form of a list of dicts
        :return: two lists, timestamps and locations
    """
    # extracts relevant datapoints from JSON; timestamps: List[float], locations: List[List[float]]
    timestamps, locations = extract_timestamps_and_locations(json_data=data)

    # pass into recognisers depending on sign
    if sign == 'A' and is_sign_a(timestamps, locations):
        return jsonify({"message": "Sign A correct"}), 200
    elif sign == 'B' and is_sign_b(timestamps, locations):
        return jsonify({"message": "Sign B correct"}), 200
    # elif sign == 'C' and is_sign_c(timestamps, locations):
    #     return jsonify({"message": "Sign B correct"}), 200

    # return statement
    return jsonify({"message": "Sign not correct"}), 200


if __name__ == '__main__':
    # Makes web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
