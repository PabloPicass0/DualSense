from typing import Callable
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from extraction import *
from sign_a.sign_a import is_sign_a
from sign_b.sign_b import is_sign_b
from sign_ch.sign_ch import is_sign_ch
import string
import time
from sign_g.sign_g import is_sign_g
from sign_h.sign_h import is_sign_h
from sign_j.sign_j import is_sign_j
from sign_ll.sign_ll import is_sign_ll
from sign_rr.sign_rr import is_sign_rr
from sign_v.sign_v import is_sign_v
from sign_w.sign_w import is_sign_w_three_curves, is_sign_w_single_curve
from sign_y.sign_y import is_sign_y
from sign_z.sign_z import is_sign_z_cubic, is_sign_z_quartic
from sign_ñ.sign_ñ import is_sign_ñ_two_curves, is_sign_ñ_single_curve
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import io
from tensorflow import keras
from ML.utils.layers import *
from typing import Optional


# define custom objects for loading keras model
custom_objects = {
    'Squash': Squash,
    'PrimaryCaps': PrimaryCaps,
    'FCCaps': FCCaps,
    'Length': Length,
    'Mask': Mask
}

# load the model (do this outside of any function, so it's only done once)
model_path = "ML/bin/model.keras"
model_STSL = keras.models.load_model(model_path, custom_objects=custom_objects)

# creates basic flask application
app = Flask(__name__)

# flask secret key for sessions to share request information;
# can be random but needs to be consistent across sessions
# for multithreading in case a Y sign comes in
app.secret_key = os.urandom(24)
# cross-Origin Resource Sharing enabled for all routes
CORS(app)

# global variable to hold the result of the first stroke for gesture 'Y'
first_stroke_result = None
# global variable to verify that a second stroke came
second_stroke_result = None

# executor for managing threads
executor = ThreadPoolExecutor(max_workers=1)


# allows client to not pass any arguments
def decorator_receive_json(executor_threads: ThreadPoolExecutor) -> Callable:
    """
    Decorator factory for injecting ThreadPoolExecutor instance into the decorated function.
    The resulting decorator will, when applied, pass the executor_threads argument to the decorated function,
    making it easy to mock or replace for testing.

    :param executor_threads: ThreadPoolExecutor instance used for managing threads.
    :return: decorator function which injects executor_threads into the decorated function.
    """

    def decorator(func):
        def wrapper():
            return func(executor_threads=executor_threads)

        return wrapper

    return decorator


# creates endpoint that listens for POST requests
@app.route('/receive_json', methods=['POST'])
@decorator_receive_json(executor)
def receive_json(executor_threads=None) -> Tuple[Response, int]:
    """
    Receives message from frontend with sign in header and touch data as JSON file.
    :rtype: tuple where first object is flask jsonify response object, second is HTTP status code
    :return: two objects: first object is flask jsonify response object, second is HTTP status code
    """

    # declare use of global variable
    global first_stroke_result
    global second_stroke_result

    # gets header/indicator for sign
    sign: string = request.headers.get('Sign')
    # gets JSON file
    data: Union[List[Dict[str, Union[float, List[float]]]], None] = request.get_json()

    # if data is none, returns error message
    if not data:
        print("not data")
        return jsonify({"message": "No JSON received"}), 400

    # saves touch data into JSON file into backend
    # with open('Templates/data.json', 'w') as file:
    #     json.dump(data, file)

    # gives json into recogniser
    # starts time measurement recognition
    start_time_param_recognition = time.time()  # capture start time recognition
    response: Tuple[Response, int] = recogniser_function(sign, data)
    end_time_param_recognition = time.time()
    print(f'Time param recognition: {end_time_param_recognition - start_time_param_recognition}')

    # if the sign is incorrect, return the response right away
    if response[0].json.get("message") == "Sign not correct":
        # if it is the second stroke for 'Y', set flag for delay_response not to reply
        if sign == 'Y' and first_stroke_result is not None:
            second_stroke_result = 'NOT'
        return response

    if sign == 'Y':
        # if a previous stroke result exists, return it and clear the result
        if first_stroke_result is not None and second_stroke_result is None:
            result = first_stroke_result
            first_stroke_result = None
            # set the flag for the second stroke for delay_response
            second_stroke_result = 'Y'
            return result

        else:
            # stores first stroke
            first_stroke_result = response

            # schedules a function to run after a delay
            future = executor_threads.submit(delay_response, app, 2)
            # blocks until the future is done, then returns its result
            return future.result()

    # returns Response (imported from Flask) and HTTP status code
    return response


def delay_response(application: Flask, delay: int) -> Tuple[Response, int]:
    """
    Delays a response to simulate asynchronous behaviour, checking the state of two global variables
    to determine the appropriate response. Note that this function directly manipulates the global variables
    'first_stroke_result' and 'second_stroke_result'.

    :param application: Flask application instance required to set up application context.
    :param delay: The delay time in seconds.
    :return: A tuple containing a Flask Response object and an HTTP status code.
    """
    with application.app_context():
        # declares use of global variables
        global first_stroke_result
        global second_stroke_result
        time.sleep(delay)
        if first_stroke_result is not None and second_stroke_result is None:
            # if no second stroke has been received after the delay
            result = (jsonify({"message": "Second stroke not received"}), 200)
            first_stroke_result = None
            return result
        elif second_stroke_result is not None:
            # if the second stroke has been received, reset second global variable
            second_stroke_result = None
            return jsonify({"message": "Second stroke already received"}), 200


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
    # elif sign == 'Ñ' and is_sign_ñ_two_curves(timestamps, locations):
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
    elif sign == 'Y' and is_sign_y(timestamps, locations):
        return jsonify({"message": "Sign Y correct"}), 200
    elif sign == 'Z' and is_sign_z_cubic(timestamps, locations):
        return jsonify({"message": "Sign Z correct"}), 200
    # elif sign == 'Z' and is_sign_z_quartic(timestamps, locations):
    #     return jsonify({"message": "Sign Z correct"}), 200

    # otherwise false
    return jsonify({"message": "Sign not correct"}), 200


@app.route('/get-template', methods=['GET'])
def get_template() -> Response:
    """
        Receives request form frontend to send corresponding template data as json file with respective coordinates.
    """
    # retrieves sign
    sign = request.args.get('sign')
    if sign:
        # reads in the coordinates and returns them
        with open(f"Templates/{sign}.json", 'r') as f:
            coordinates = json.load(f)
            return jsonify(coordinates)
    else:
        return jsonify(["No sign available"])


@app.route('/save-sample', methods=['POST'])
def save_sample() -> Response:
    """
    Receives image data from the frontend and stores it in the "Dataset" folder.
    """
    # checks if the 'Filename' header is provided
    filename: str = request.headers.get('Filename')
    if not filename:
        return Response("No filename provided", status=400)

    # gets image data from the request
    image_data = request.data
    if not image_data:
        return Response("No png received", status=400)

    # creates the "Dataset" directory if it doesn't exist
    os.makedirs('ML/Dataset', exist_ok=True)

    # saves the image to the "Dataset" directory with the provided filename
    file_path = os.path.join('ML/Dataset', filename + '.png')
    with open(file_path, 'wb') as file:
        file.write(image_data)

    return Response("Image saved successfully", status=200)


@app.route('/detect-gesture-ml', methods=['POST'])
def recogniser_function_ml() -> Response:
    """
    Receives gesture screenshot, feeds it into model, and returns classification.
    """
    # extract image
    user_gesture = request.data
    if not user_gesture:
        return Response("No png received", status=400)

    # starts time measurement
    start_time_ml_recognition = time.time()  # capture start time

    # preprocess image
    user_gesture_preprocessed = preprocess_image(user_gesture)
    user_gesture_preprocessed = np.expand_dims(user_gesture_preprocessed, axis=0)

    # predict label with model
    y_pred, img_reconstructed = model_STSL.predict(user_gesture_preprocessed)
    # ends time measurement
    end_time_ml_recognition = time.time()  # capture end time
    print(f'Time ml recognition: {end_time_ml_recognition - start_time_ml_recognition}')

    # plot and save the reconstructed image
    plt.imshow(img_reconstructed[0].reshape(128, 128), cmap='gray')
    plt.axis('off')  # turn off the axis
    plt.savefig('reconstructed_image.png', bbox_inches='tight', pad_inches=0)

    # print whole prediction array for debugging
    print(y_pred)

    # convert prediction into meaningful label
    label = extract_label(y_pred)

    print(f"label extracted: {label}")

    # return output
    if label:
        response_message = f"Sign {label} recognised"
    else:
        response_message = f"No sign recognised"
    return Response(response_message, status=200)


def preprocess_image(image_data: bytes) -> np.ndarray:
    """
    Preprocesses the given image data: Converts it to grayscale, resizes to 128x128, converts to a numpy array,
    normalizes pixel values to [0, 1].

    :params image_data (bytes): The raw image data.
    :return: np.ndarray: The preprocessed image in numpy array format.
    """

    # decode the image and convert to grayscale
    image: Image.Image = Image.open(io.BytesIO(image_data)).convert('L')

    # resize the image to 128x128
    image = image.resize((128, 128))

    # convert to numpy array
    image_array: np.ndarray = np.array(image)

    # normalise the pixel values to [0, 1]
    image_array = image_array / 255.0

    # add the channel dimension
    image_array = image_array[..., None]

    return image_array


def extract_label(y_pred: np.ndarray, label_mapping: Dict[str, int] = None) -> Optional[str]:
    """
    Extracts the label corresponding to the highest prediction value.

    :param y_pred: The prediction array from the model.
    :param label_mapping: Dictionary containing mapping of labels to their respective integers.
    :return: The predicted label as a string or None.
    """
    # if no label mapping is provided, use the default one
    if label_mapping is None:
        label_mapping = {'CH': 0, 'G': 1, 'H': 2, 'J': 3, 'LL': 4, 'Ñ': 5, 'RR': 6, 'V': 7, 'W': 8, 'Z': 9, 'Y': 10}

    # reverse the label_mapping dictionary for easy lookup
    reverse_label_mapping = {v: k for k, v in label_mapping.items()}

    # if the max prediction value is below 0.9, return None
    max_probability = np.max(y_pred)
    if max_probability < 0.9:
        return None

    # get the index of the maximum prediction value
    class_probabilities = y_pred
    predicted_class_index = np.argmax(class_probabilities)

    print(f'With probability: {max_probability}')

    # fetch the label from the reverse mapping
    predicted_label = reverse_label_mapping[predicted_class_index]

    return predicted_label


if __name__ == '__main__':
    # make web server listen on port 5000 and makes it externally visible by binding it to 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
