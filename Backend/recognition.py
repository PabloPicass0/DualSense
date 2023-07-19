from typing import List

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


def timestamp_duration_valid(sign: str, timestamps: List[float]) -> bool:
    """
    Checks whether the difference between the first and the last timestamp is larger than a given time period,
    depending on the sign.

    :param sign: A string, indicating which sign is parsed.
    :param timestamps: List of timestamps
    :return: True if the duration is less than or equal to 3 seconds, False otherwise
    """
    time_period = 2

    if sign == 'LL':
        time_period = 4
    elif sign == 'Ñ':
        time_period = 4
    elif sign == 'RR':
        time_period = 4
    elif sign == 'W':
        time_period = 4
    elif sign == 'Y':
        time_period = 1
    elif sign == 'Z':
        time_period = 3

    return timestamps[-1] - timestamps[0] <= time_period


def compare_sequences(seq1: np.ndarray, seq2: np.ndarray) -> float:
    """
    Compares two sequences using Dynamic Time Warping.

    :param seq1: The first sequence. It is a numpy array.
    :param seq2: The second sequence. It is a numpy array.
    :return: The Dynamic Time Warping distance between the sequences as a float.
    """
    distance, _ = fastdtw(seq1, seq2, dist=euclidean)

    return distance
