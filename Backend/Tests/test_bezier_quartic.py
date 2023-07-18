import pytest

from parameterisation import *


def test_error_function_quartic():
    """Verifies that the sum of the squares is computed correctly for a simple case"""
    # defines the control points, coordinates and times
    control = np.array([[1, 1], [2, 2], [3, 3]])
    coordinates = np.array([[1, 1], [1, 1]])
    # for t = 0 the Bézier curve amounts to P0; to get 0, coordinates must be = P0
    times = np.zeros(2)

    # calls the function with the test parameters
    # calculates difference between original points and estimates
    result = error_function_quartic(control, coordinates, times)

    # Check if the result is as expected
    assert np.allclose(result, 0), "Test failed"


def test_fit_quartic_bezier_control_points():
    """Simple test that shows that a straight line of coordinates yields a straight curve"""
    # defines the coordinates
    coordinates = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]

    # calls the function with the test parameters
    result = fit_quartic_bezier_control_points(coordinates)

    # checks if the result is as expected
    # the control points for a quartic Bézier curve fitting the straight line should also form a straight line.
    expected_result = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
    assert np.allclose(result, expected_result), "Test failed"


def test_calculate_quartic_bezier_curve_point():
    """Simple test that checks of the point at t=0.5 is the middle point."""
    # defines the control points for a quartic Bézier curve
    control_points = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])

    # calls the function with the test parameter
    t = 0.5  # halfway along the curve
    result = calculate_quartic_bezier_curve_point(t, control_points)

    # the result should be halfway between the start and end points for this simple curve
    expected_result = np.array([2, 2])

    # checks if the result is as expected
    assert np.allclose(result, expected_result), "Test failed"


def test_return_quartic_bezier_curve():
    """Simple test that checks whether the correct number of points is generated and if the first and last points match.
    """
    # defines the control points for a simple curve
    control_points = np.array([[0, 0], [1, 2], [2, 2], [3, 2], [4, 0]])
    num_points = 50

    # calls the function with the test parameters
    result = return_quartic_bezier_curve(control_points, num_points)

    # checks if the correct number of points was generated
    assert len(result) == num_points, "Number of points generated is not as expected"

    # checks if the first point is the first control point and the last point is the last control point
    assert np.allclose(result[0], control_points[0]), "First point generated is not the first control point"
    assert np.allclose(result[-1], control_points[-1]), "Last point generated is not the last control point"


if __name__ == '__main__':
    pytest.main()
