import math
from typing import List

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from dtw import *
import time


def timestamp_duration_valid(sign: str, timestamps: List[float]) -> bool:
    """
    Checks whether the difference between the first and the last timestamp is larger than a given time period,
    depending on the sign.

    :param sign: A string, indicating which sign is parsed.
    :param timestamps: List of timestamps
    :return: True if the duration is less than or equal to 3 seconds, False otherwise
    """
    time_period = 2
    if sign == 'CH':
        time_period = 2
    elif sign == 'G':
        time_period = 2
    elif sign == 'H':
        time_period = 2
    elif sign == 'J':
        time_period = 2
    elif sign == 'LL':
        time_period = 4
    elif sign == 'RR':
        time_period = 4
    elif sign == 'V':
        time_period = 2
    elif sign == 'W':
        time_period = 4
    elif sign == 'Y':
        time_period = 1
    elif sign == 'Z':
        time_period = 3
    elif sign == 'Ñ':
        time_period = 4

    return timestamps[-1] - timestamps[0] <= time_period


def compare_sequences_fdtw(seq1: np.ndarray, seq2: np.ndarray) -> float:
    """
    Compares two sequences (Bézier curves) using Dynamic Time Warping.

    :param seq1: The first sequence. It is a numpy array.
    :param seq2: The second sequence. It is a numpy array.
    :return: The Dynamic Time Warping distance between the sequences as a float.
    """
    # start_time = time.time()  # capture start time
    distance, _ = fastdtw(seq1, seq2, dist=euclidean)
    # end_time = time.time()  # capture end time
    # print(f"FastDTW takes {end_time - start_time} seconds.")

    return distance


# function below not working
# def compare_sequences_dtw(seq1: np.ndarray, seq2: np.ndarray) -> float:
#     """
#     Compares two sequences (Bézier curves) using Dynamic Time Warping.
#
#     :param seq1: The first sequence. It is a numpy array.
#     :param seq2: The second sequence. It is a numpy array.
#     :return: The Dynamic Time Warping distance between the sequences as a float.
#     """
#     start_time = time.time()  # capture start time
#     alignment = dtw(seq1, seq2)
#     end_time = time.time() # capture end time
#     print(f"The operation took {end_time - start_time} seconds.")
#     distance = alignment[0]  # accessing the first element of the tuple
#
#     return distance


def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """
    Calculates the Euclidean distance between two points in 2D.

    :param point1: The first point as a tuple of two floats representing x and y coordinates.
    :param point2: The second point as a tuple of two floats representing x and y coordinates.

    :return: The Euclidean distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
