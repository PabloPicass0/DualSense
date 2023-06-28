from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from extraction import *
from sign_a import is_sign_a

# Creates basic flask application
app = Flask(__name__)
# Cross-Origin Resource Sharing enabled for all routes
CORS(app)


# Creates endpoint that listens for POST requests
@app.route('/receive_json', methods=['POST'])
def receive_json() -> Tuple[Response, int]:
    # gets JSON file
    data: Union[List[Dict[str, Union[float, List[float]]]], None] = request.get_json()
    # if data is none, returns error message
    if not data:
        print("not data")
        return jsonify({"message": "No JSON received"}), 400

    # extracts relevant datapoints from JSON; timestamps: List[float], locations: List[List[float]]
    timestamps, locations = extract_timestamps_and_locations(json_data=data)
    # give into recogniser for respective sign
    if is_sign_a(timestamps, locations):
        # if successful, return success message
        return jsonify({"message": "Sign correct"}), 200

    # returns Response (imported from Flask) and HTTP status code
    return jsonify({"message": "Sign not correct"}), 200


if __name__ == '__main__':
    # Makes web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
