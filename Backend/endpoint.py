from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from extraction import *
from sign_a import is_sign_a
from sign_b import is_sign_b
from sign_ch.sign_ch import is_sign_ch
import string

from sign_g.sign_g import is_sign_g
from sign_h.sign_h import is_sign_h
from sign_j.sign_j import is_sign_j
from sign_ll.sign_ll import is_sign_ll
from sign_rr.sign_rr import is_sign_rr
from sign_v.sign_v import is_sign_v
from sign_w.sign_w import is_sign_w_three_curves, is_sign_w_single_curve
from sign_z.sign_z import is_sign_z_cubic, is_sign_z_quartic
from sign_ñ.sign_ñ import is_sign_ñ, is_sign_ñ_single_curve

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

    # if data is none, returns error message
    if not data:
        print("not data")
        return jsonify({"message": "No JSON received"}), 400

    # saves touch data into JSON file into backend
    with open('data.json', 'w') as file:
        json.dump(data, file)

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
    elif sign == 'CH' and is_sign_ch(timestamps, locations):
        return jsonify({"message": "Sign CH correct"}), 200
    elif sign == 'G' and is_sign_g(timestamps, locations):
        return jsonify({"message": "Sign G correct"}), 200
    elif sign == 'H' and is_sign_h(timestamps, locations):
        return jsonify({"message": "Sign H correct"}), 200
    elif sign == 'J' and is_sign_j(timestamps, locations):
        return jsonify({"message": "Sign J correct"}), 200
    elif sign == 'LL' and is_sign_ll(timestamps, locations):
        return jsonify({"message": "Sign LL correct"}), 200
    # elif sign == 'Ñ' and is_sign_ñ(timestamps, locations):
    #     return jsonify({"message": "Sign Ñ correct"}), 200
    elif sign == 'Ñ' and is_sign_ñ_single_curve(timestamps, locations):
        return jsonify({"message": "Sign Ñ correct"}), 200
    elif sign == 'RR' and is_sign_rr(timestamps, locations):
        return jsonify({"message": "Sign RR correct"}), 200
    elif sign == 'V' and is_sign_v(timestamps, locations):
        return jsonify({"message": "Sign V correct"}), 200
    # elif sign == 'W' and is_sign_w_single_curve(timestamps, locations):
    #     return jsonify({"message": "Sign W correct"}), 200
    elif sign == 'W' and is_sign_w_three_curves(timestamps, locations):
        return jsonify({"message": "Sign W correct"}), 200
    elif sign == 'Z' and is_sign_z_cubic(timestamps, locations):
        return jsonify({"message": "Sign Z correct"}), 200
    # elif sign == 'Z' and is_sign_z_quartic(timestamps, locations):
    #     return jsonify({"message": "Sign Z correct"}), 200

    # otherwise false
    return jsonify({"message": "Sign not correct"}), 200


@app.route('/get-template', methods=['GET'])
def get_template():
    """
        Receives request form frontend to send corresponding template data as json file with respective coordinates.
    """
    # retrieves sign
    sign = request.args.get('sign')
    if sign:
        # reads in the coordinates and returns them
        with open(f"{sign}.json", 'r') as f:
            coordinates = json.load(f)
            return jsonify(coordinates)
    else:
        return jsonify(["No sign available"])


if __name__ == '__main__':
    # Makes web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
