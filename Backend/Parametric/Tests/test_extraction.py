import pytest

from extraction import extract_timestamps_and_locations, split_touch_locations_two_curves, \
    split_touch_locations_three_curves
from recognition import euclidean_distance


def test_extract_timestamps_and_locations():
    json_data = [{'timestamp': 1.0, 'location': [0.0, 1.0]},
                 {'timestamp': 2.0, 'location': [1.0, 2.0]}]

    expected_timestamps = [1.0, 2.0]
    expected_locations: list[list[float]] = [[0.0, 1.0], [1.0, 2.0]]

    timestamps, locations = extract_timestamps_and_locations(json_data)

    assert timestamps == expected_timestamps
    assert locations == expected_locations


def test_split_touch_locations_two_curves():
    # Mock data
    locations = [[0, 0], [1, 1], [2, 2], [3, 3], [110, 110], [111, 111]]

    # Test for 'LL'
    sign = 'LL'
    curve1, curve2 = split_touch_locations_two_curves(sign, locations)
    assert curve1 == [[0, 0], [1, 1], [2, 2], [3, 3]]
    assert curve2 == [[110, 110], [111, 111]]

    # Test for 'RR'
    sign = 'RR'
    curve1, curve2 = split_touch_locations_two_curves(sign, locations)
    assert curve1 == [[0, 0], [1, 1], [2, 2], [3, 3]]
    assert curve2 == [[110, 110], [111, 111]]

    # Test for error case
    with pytest.raises(ValueError):
        locations = [[0, 0], [1, 1], [2, 2], [3, 3]]
        curve1, curve2 = split_touch_locations_two_curves(sign, locations)


def test_split_touch_locations_three_curves():
    locations = [[0, 0], [10, 10], [20, 20], [60, 60], [65, 65], [110, 110], [120, 120], [70, 70], [125, 125], [5, 5]]

    curve1, curve2, curve3 = split_touch_locations_three_curves(locations)

    print(curve1)
    print(curve2)
    print(curve3)

    assert curve1 is not None, "curve1 should not be None"
    assert curve2 is not None, "curve2 should not be None"
    assert curve3 is not None, "curve3 should not be None"

    assert len(curve1) == 4, "curve1 should not be empty"
    assert len(curve2) == 3, "curve2 should not be empty"
    assert len(curve3) == 3, "curve3 should not be empty"

    # checks if points are correctly distributed among the curves based on the thresholds
    assert euclidean_distance(curve1[-1], curve2[0]) > 25
    assert euclidean_distance(curve2[-1], curve3[0]) > 25


if __name__ == '__main__':
    pytest.main()
