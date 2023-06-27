# Creates basic flask application
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Cross-Origin Resource Sharing enabled for all routes
CORS(app)


# Creates endpoint that listens for POST requests
@app.route('/receive_json', methods=['POST'])
def receive_json():
    print("receive json called")
    # Gets JSON file, prints it, and returns "received"
    data = request.get_json()
    if not data:
        print("not data")
        return jsonify({"message": "No JSON received"}), 400
    # Process your data here
    print(data)
    return jsonify({"message": "JSON received"}), 200


if __name__ == '__main__':
    # Makes web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
