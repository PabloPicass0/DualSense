import numpy as np
import pytest

from extraction import split_touch_locations_two_curves
from parameterisation import linear_bezier_curve, generate_two_linear_beziers


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


def test_generate_two_linear_beziers():
    # tests this with simple set of coordinates
    locations = [[0, 0], [1, 1], [2, 2], [20, 20], [21, 21], [22, 22]]
    curve1, curve2 = split_touch_locations_two_curves('CH', locations)
    bezier1, bezier2 = generate_two_linear_beziers(curve1, curve2)

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


if __name__ == '__main__':
    pytest.main()
