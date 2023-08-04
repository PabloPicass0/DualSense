import math

import numpy as np
import pytest

from recognition import euclidean_distance, compare_sequences_fdtw


def test_euclidean_distance():
    point1 = [0, 0]
    point2 = [1, 1]
    assert math.isclose(euclidean_distance(point1, point2), math.sqrt(2)), "The distance should be sqrt(2)."

    point1 = [0, 0]
    point2 = [0, 0]
    assert euclidean_distance(point1, point2) == 0, "The distance between two identical points should be 0."

    point1 = [-1, -1]
    point2 = [1, 1]
    assert math.isclose(euclidean_distance(point1, point2), 2 * math.sqrt(2)), "The distance should be 2 * sqrt(2)."

    point1 = [-1.5, 3.4]
    point2 = [4.2, -1.6]
    result = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    assert math.isclose(euclidean_distance(point1, point2), result), f"The distance should be {result}."


def test_compare_sequences():
    # tests two identical sequences
    seq1 = np.array([[0, 0], [1, 1], [2, 2]])
    seq2 = np.array([[0, 0], [1, 1], [2, 2]])
    assert compare_sequences_fdtw(seq1, seq2) == 0, "identical sequences should have 0 distance"

    # tests two completely different sequences
    seq3 = np.array([[3, 3], [4, 4], [5, 5]])
    assert compare_sequences_fdtw(seq1, seq3) > 0, "different sequences should have > 0 distance"


if __name__ == '__main__':
    pytest.main()
