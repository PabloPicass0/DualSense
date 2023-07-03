import pytest
from Backend.sign_ch.sign_ch import *


def test_linear_bezier_curve():
    # defines the control points
    p0 = np.array([1, 1])
    p1 = np.array([2, 2])

    # defines the parameter values
    t = np.linspace(0, 1, num=100)

    # calls the function
    curve = linear_bezier_curve(p0, p1, t)

    # now test that the curve starts at p0 and ends at p1
    assert np.allclose(curve[0], p0), "The curve should start at the first control point."
    assert np.allclose(curve[-1], p1), "The curve should end at the second control point."

    # checks that the shape of the curve is as expected
    assert curve.shape == (
        100, 2), "The curve should have as many points as the number of parameter values, and each point should be 2D."

    # test that the curve is a straight line
    slopes = np.diff(curve, axis=0)  # calculate the slope between every two consecutive points
    assert np.allclose(slopes, slopes[
        0]), "For a linear Bézier curve, the slope should be the same between every two consecutive points."


def test_euclidean_distance():
    point1 = (0, 0)
    point2 = (1, 1)
    assert math.isclose(euclidean_distance(point1, point2), math.sqrt(2)), "The distance should be sqrt(2)."

    point1 = (0, 0)
    point2 = (0, 0)
    assert euclidean_distance(point1, point2) == 0, "The distance between two identical points should be 0."

    point1 = (-1, -1)
    point2 = (1, 1)
    assert math.isclose(euclidean_distance(point1, point2), 2 * math.sqrt(2)), "The distance should be 2 * sqrt(2)."

    point1 = (-1.5, 3.4)
    point2 = (4.2, -1.6)
    result = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    assert math.isclose(euclidean_distance(point1, point2), result), f"The distance should be {result}."


def test_split_touch_locations():
    locations = [(0, 0), (1, 1), (2, 2), (20, 20), (21, 21), (22, 22)]
    curve1, curve2 = split_touch_locations(locations)
    assert curve1 == [(0, 0), (1, 1), (2, 2)], "First three points should be in curve1."
    assert curve2 == [(20, 20), (21, 21), (22, 22)], "Last three points should be in curve2."

    locations = [(0, 0), (11, 11), (22, 22), (33, 33), (44, 44)]
    curve1, curve2 = split_touch_locations(locations)
    assert curve1 == [(0, 0)], "Only first point should be in curve1."
    assert curve2 == [(11, 11), (22, 22), (33, 33), (44, 44)], "Remaining points should be in curve2."

    locations = [(0, 0), (5, 5), (10, 10), (15, 15), (20, 20)]
    curve1, curve2 = split_touch_locations(locations)
    assert curve1 == locations, "All points should be in curve1 as they're within 10 units of each other."
    assert curve2 == [], "Curve2 should be empty."


def test_generate_two_linear_beziers():
    # tests this with simple set of coordinates
    locations = [(0, 0), (1, 1), (2, 2), (20, 20), (21, 21), (22, 22)]
    bezier1, bezier2 = generate_two_linear_beziers(locations)

    # checks that the output are numpy arrays
    assert isinstance(bezier1, np.ndarray), "Output bezier1 is not a numpy array"
    assert isinstance(bezier2, np.ndarray), "Output bezier2 is not a numpy array"

    # checks that the shapes of the output arrays are correct
    assert bezier1.shape[1] == 2, "Output bezier1 does not have 2 columns (for x, y)"
    assert bezier2.shape[1] == 2, "Output bezier2 does not have 2 columns (for x, y)"

    # checks that the start and end points of the Bézier curves match the start and end points of the input locations
    np.testing.assert_allclose(bezier1[0, :], locations[0],
                               err_msg="bezier1 does not start at the same point as locations")
    np.testing.assert_allclose(bezier1[-1, :], locations[2],
                               err_msg="bezier1 does not end at the same point as locations")

    np.testing.assert_allclose(bezier2[0, :], locations[3],
                               err_msg="bezier2 does not start at the same point as locations")
    np.testing.assert_allclose(bezier2[-1, :], locations[-1],
                               err_msg="bezier2 does not end at the same point as locations")


def test_compare_sequences():
    # tests two identical sequences
    seq1 = np.array([[0, 0], [1, 1], [2, 2]])
    seq2 = np.array([[0, 0], [1, 1], [2, 2]])
    assert compare_sequences(seq1, seq2) == 0, "identical sequences should have 0 distance"

    # tests two completely different sequences
    seq3 = np.array([[3, 3], [4, 4], [5, 5]])
    assert compare_sequences(seq1, seq3) > 0, "different sequences should have > 0 distance"


def test_is_sign_ch():
    # Test case: invalid gesture; just one curve
    timestamps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    locations = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
    assert not is_sign_ch(timestamps, locations), "The function should return False for a gesture with only one curve"

    # Test case: invalid gesture (with time frame too long)
    timestamps = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    locations = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
    assert not is_sign_ch(timestamps, locations), "The function should return False for an invalid gesture"

    # Test case: invalid gesture because of strong differences
    timestamps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    locations = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [100, 100], [101, 101], [102, 102], [103, 103], [104, 104]]
    assert not is_sign_ch(timestamps, locations), "The function should return True for a valid gesture with two curves"


if __name__ == '__main__':
    pytest.main()
