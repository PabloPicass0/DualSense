import pytest
from ..extraction import *


def test_extract_timestamps_and_locations():
    json_data = [{'timestamp': 1.0, 'location': [0.0, 1.0]},
                 {'timestamp': 2.0, 'location': [1.0, 2.0]}]

    expected_timestamps = [1.0, 2.0]
    expected_locations: list[list[float]] = [[0.0, 1.0], [1.0, 2.0]]

    timestamps, locations = extract_timestamps_and_locations(json_data)

    assert timestamps == expected_timestamps
    assert locations == expected_locations
