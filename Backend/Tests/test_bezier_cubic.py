import numpy as np
import pytest

from parameterisation import calculate_cubic_bezier_point, fit_cubic_bezier_curve, error_function_cubic


def test_calculate_cubic_bezier_point():
    # defines some points for testing
    p0 = np.array([0, 0])
    p1 = np.array([1, 1])
    p2 = np.array([2, 1])
    p3 = np.array([3, 0])

    # testing for t=0, it should return the first point p0
    assert np.array_equal(calculate_cubic_bezier_point(0, p0, p1, p2, p3), p0)

    # testing for t=1, it should return the last point p3
    assert np.array_equal(calculate_cubic_bezier_point(1, p0, p1, p2, p3), p3)

    # testing for t=0.5, it should return the point on the curve at t=0.5
    expected_result = 0.125 * p0 + 0.375 * p1 + 0.375 * p2 + 0.125 * p3
    assert np.allclose(calculate_cubic_bezier_point(0.5, p0, p1, p2, p3), expected_result)


def test_error_function_cubic():
    # defines end points
    p0 = np.array([0, 0])
    p3 = np.array([3, 0])

    # defines times
    times = np.linspace(0, 1, 4)

    # defines a perfect cubic Bezier curve
    perfect_curve = np.array([calculate_cubic_bezier_point(t, p0, np.array([1, 1]), np.array([2, 1]), p3)
                              for t in times])

    # calculates control points from perfect curve
    control = fit_cubic_bezier_curve(perfect_curve)[1:3].flatten()

    # testing for perfectly fitting curve, error should be close to 0
    assert np.allclose(error_function_cubic(control, perfect_curve, times), 0, atol=1e-8)

    # testing for not perfectly fitting curve, error should be > 0
    imperfect_curve = np.array([p0, np.array([1, 1]), np.array([2, 2]), p3])  # p2 is shifted to create an imperfect
    # curve
    assert error_function_cubic(control, imperfect_curve, times) > 0


def test_fit_cubic_bezier_curve():
    # defines some coordinates for testing
    coordinates = [[0, 0], [1, 1], [2, 1], [3, 0]]

    # fits a cubic Bézier curve to the coordinates
    bezier_control_points = fit_cubic_bezier_curve(coordinates)

    # defines an array of times between 0 and 1
    times = np.linspace(0, 1, len(coordinates))

    # recreates the curve from the control points
    recreated_curve = [calculate_cubic_bezier_point(t, *bezier_control_points) for t in times]

    # compares the recreated curve to the original coordinates
    assert np.allclose(recreated_curve, coordinates,
                       atol=1e-6), f"Recreated curve {recreated_curve} does not match original " \
                                   f"coordinates {coordinates} within tolerance"


if __name__ == '__main__':
    pytest.main()
