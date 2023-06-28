"""
Functions to extract data and features from JSON files.
"""

from typing import List, Dict, Tuple, Union


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
