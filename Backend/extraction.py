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


# Call the function
if __name__ == '__main__':
    numpy_to_json('sign_ch', 'bezier2_lower_curve_template.npy')