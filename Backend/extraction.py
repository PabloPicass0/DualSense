"""
Functions to extract data and features from JSON files.
"""
import json
import math
import os
from typing import List, Dict, Tuple, Union

import numpy as np


def extract_timestamps_and_locations(json_data: List[Dict[str, Union[float, List[float]]]]) -> Tuple[
    List[float], List[List[float]]]:
    """
    Extracts timestamps and locations into two individual arrays
    :rtype: tuple
    :param json_data: the touch data detected by the touch screen, in form of a list of dicts
    :return: two lists, timestamps and locations
    """

    # initializes empty lists
    timestamps = []
    locations = []

    # appends timestamps and locations
    for item in json_data:
        timestamps.append(item['timestamp'])
        locations.append(item['location'])

    return timestamps, locations


def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """
    Calculates the Euclidean distance between two points in 2D.

    :param point1: The first point as a tuple of two floats representing x and y coordinates.
    :param point2: The second point as a tuple of two floats representing x and y coordinates.

    :return: The Euclidean distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def split_touch_locations(sign: str, locations: List[List[float]]) -> Tuple[
    List[List[float]], List[List[float]]]:
    """
    Splits the provided locations into two curves based on a distance threshold, depending on the sign.

    :param sign: A string indicating which sign is parsed.
    :param locations: A list of tuples, each representing the (x, y) coordinates of a point.

    :return: Two lists of tuples, each list represents a curve and each tuple within the list represents a point on the
    curve.
    """
    curve1 = []
    curve2 = []

    # defines threshold
    threshold = 10

    # assigns value to threshold depending on curve
    if sign == 'LL':
        # both curves are far from each other for LL
        threshold = 100
    elif sign == 'Ñ':
        # curves are closer together
        threshold = 20
    elif sign == 'RR' or sign == 'V':
        # medium distance
        threshold = 50

    # starts by putting the first point in curve1
    curve1.append(locations[0])
    for i in range(1, len(locations)):
        # assigns point to either curve1 or curve2 depending on distance
        if euclidean_distance(locations[i], curve1[-1]) <= threshold:
            curve1.append(locations[i])
        else:
            curve2.append(locations[i])

    # raises error if curve2 is empty
    if not curve2:
        raise ValueError("Curve2 is empty.")

    return curve1, curve2


def numpy_to_json(directory: str, filename: str):
    """
    This function loads a NumPy array from a file, converts it into a list (since NumPy arrays
    are not JSON serializable), and then saves it as a JSON file in the current directory.

    :param directory: The directory where the .npy file is stored.
    :param filename: The name of the .npy file.
    """
    # loads numpy array
    numpy_data = np.load(os.path.join(directory, filename))

    # converts numpy array to list
    data_as_list = numpy_data.tolist()

    # saves as json
    with open(filename.split('.')[0] + '.json', 'w') as json_file:
        json.dump(data_as_list, json_file)


def read_and_store_locations_to_json(directory: str, filename: str, output_filename: str):
    """
    This function loads data from a JSON file, separates locations from timestamps using the
    existing function, and stores the locations into a new JSON file.

    :param directory: The directory where the input JSON file is stored.
    :param filename: The name of the input JSON file.
    :param output_filename: The name of the output JSON file for locations.
    """
    # loads data from JSON file
    with open(os.path.join(directory, filename), 'r') as json_file:
        data = json.load(json_file)

    # splits data into timestamps and locations
    _, locations = extract_timestamps_and_locations(data)

    # saves locations as JSON
    with open(os.path.join(directory, output_filename), 'w') as json_file:
        json.dump(locations, json_file)


if __name__ == '__main__':
    # extracts numpy template (Bézier curves) into json file for frontend
    numpy_to_json('sign_v', 'bezier2_curve_template.npy')

# extracts touch location coordinates into json files
# make sure to update the filename before use to not override other files
# read_and_store_locations_to_json('.', 'data.json', 'ñ.json')
