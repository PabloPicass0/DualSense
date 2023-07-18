import pytest

from extraction import extract_timestamps_and_locations, split_touch_locations


def test_extract_timestamps_and_locations():
    json_data = [{'timestamp': 1.0, 'location': [0.0, 1.0]},
                 {'timestamp': 2.0, 'location': [1.0, 2.0]}]

    expected_timestamps = [1.0, 2.0]
    expected_locations: list[list[float]] = [[0.0, 1.0], [1.0, 2.0]]

    timestamps, locations = extract_timestamps_and_locations(json_data)

    assert timestamps == expected_timestamps
    assert locations == expected_locations


def test_split_touch_locations():
    # Mock data
    locations = [[0, 0], [1, 1], [2, 2], [3, 3], [110, 110], [111, 111]]

    # Test for 'LL'
    sign = 'LL'
    curve1, curve2 = split_touch_locations(sign, locations)
    assert curve1 == [[0, 0], [1, 1], [2, 2], [3, 3]]
    assert curve2 == [[110, 110], [111, 111]]

    # Test for 'RR'
    sign = 'RR'
    curve1, curve2 = split_touch_locations(sign, locations)
    assert curve1 == [[0, 0], [1, 1], [2, 2], [3, 3]]
    assert curve2 == [[110, 110], [111, 111]]

    # Test for error case
    with pytest.raises(ValueError):
        locations = [[0, 0], [1, 1], [2, 2], [3, 3]]
        curve1, curve2 = split_touch_locations(sign, locations)


if __name__ == '__main__':
    pytest.main()
