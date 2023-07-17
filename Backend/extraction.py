"""
Functions to extract data and features from JSON files.
"""
import json
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


# calls the function
# if __name__ == '__main__':
    # extracts numpy template (Bézier curves) into json file for frontend
    # numpy_to_json('sign_j', 'bezier_curve_template.npy')

    # extracts touch location coordinates into json files
    # make sure to update the filename before use to not override other files
    # read_and_store_locations_to_json('.', 'data.json', 'ñ.json')
