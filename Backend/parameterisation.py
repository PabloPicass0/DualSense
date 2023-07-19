from typing import List, Tuple

import numpy as np
from scipy.optimize import minimize

""" ******************************************* Linear Bezier function ******************************************* """


def linear_bezier_curve(p0: np.ndarray, p1: np.ndarray, t: np.ndarray) -> np.ndarray:
    """
    Function to calculate a linear Bézier curve.

    :param p0: The starting control point of the Bézier curve. It is a numpy array.
    :param p1: The ending control point of the Bézier curve. It is a numpy array.
    :param t: The parameter values, typically ranging from 0 to 1. It is a numpy array.

    :return: The computed Bézier curve as a numpy array.
    """
    return (1 - t)[:, None] * p0 + t[:, None] * p1


def generate_linear_bezier(locations: List[List[float]]) -> np.ndarray:
    """
    Generates one linear Bézier curve given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: One numpy array,representing a linear Bézier curve.
    """

    # control points: fits curves into linear Bézier curve
    P0_curve = np.array(locations[0])
    P1_curve = np.array(locations[-1])

    # assigns parameter values
    t = np.linspace(0, 1, num=100)

    # calculates points for curve1
    bezier = linear_bezier_curve(P0_curve, P1_curve, t=t)

    return bezier


""" ******************************************* Qubic Bezier function ******************************************* """


def calculate_cubic_bezier_point(t: float, p0: np.array, p1: np.array, p2: np.array, p3: np.array) -> np.array:
    """
    Calculates a point on a cubic Bézier curve.

    :param t: The parameter t in the range of [0, 1] for calculating a point on the Bézier curve.
    :param p0: The first endpoint of the Bézier curve.
    :param p1: The first control point of the Bézier curve.
    :param p2: The second control point of the Bézier curve.
    :param p3: The second endpoint of the Bézier curve.
    :return: The calculated point on the curve.
    """
    # cubic Bézier formula to compute a point on the curve
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def error_function_cubic(control: np.array, coordinates: np.ndarray, times: np.ndarray) -> np.array:
    """
    Error function for the cubic curve fitting optimization problem.

    :param control: Control points for cubic Bézier curve.
    :param coordinates: Coordinates through which the curve should pass.
    :param times: Array of equally spaced time instances.
    :return: The calculated error.
    """
    # separates end and control points
    p0, p3 = coordinates[0], coordinates[-1]
    p1, p2 = control.reshape(2, -1)

    # estimates the curve points by calculating Bézier points for all time values
    estimate = np.array([calculate_cubic_bezier_point(t, p0, p1, p2, p3) for t in times])

    # calculates and return the error as sum of squares of the difference between coordinates and estimate
    return np.sum((coordinates - estimate) ** 2)


def fit_cubic_bezier_curve(coordinates: List[List[float]]) -> np.ndarray:
    """
    Fits a cubic Bézier curve to the given coordinates.

    :param coordinates: A list of touch locations, where each location is a list of x and y coordinates.
    :return: The four control points of a cubic Bézier curve.
    """
    # converts to numpy for numerical calculations
    coordinates_np = np.array(coordinates)
    # creates an array with equally spaced times between 0 and 1 to parametrize the Bézier curve
    times = np.linspace(0, 1, len(coordinates_np))

    # uses the mean of all coordinates as the initial guess for the control points of the Bézier curve
    # the initial guess has four points (hence the repeat)
    initial_guess = np.repeat(coordinates_np.mean(axis=0), 2)

    # uses the BFGS method to minimize the error function and returns the optimal control points that
    # minimize the difference between the Bézier curve and the given coordinates.
    result = minimize(error_function_cubic, initial_guess, args=(coordinates_np, times), method='BFGS')
    control = result.x.reshape(2, -1)
    return np.array([coordinates_np[0], control[0], control[1], coordinates_np[-1]])


def return_cubic_bezier(locations: List[List[float]]) -> List[np.ndarray]:
    """
    Calculates the control points for the curve, generates 100 evenly spaced points,
    and calculates the corresponding point on the Bézier curve for each 't' using the control points.

    :param locations: Locations through which the curve should pass.
    :return: The calculated curve points.
    """
    # calculates the control points for the curve
    bezier_control_points = fit_cubic_bezier_curve(locations)
    # generates 100 evenly spaced points, representing the parameter t
    t_values = np.linspace(0, 1, 100)
    # calculates the corresponding point on the Bézier curve for each 't' using the control points
    curve_points = [calculate_cubic_bezier_point(t, *bezier_control_points) for t in t_values]
    return curve_points


""" ******************************************* Quartic Bezier function ******************************************* """


def error_function_quartic(control: np.array, coordinates: np.ndarray, times: np.ndarray) -> np.array:
    """
    Error function for the quartic curve fitting optimization problem.

    :param control: Control points for quartic Bézier curve.
    :param coordinates: Coordinates through which the curve should pass.
    :param times: Array of equally spaced time instances.
    :return: The calculated error.
    """
    # separates end and control points
    p0, p4 = coordinates[0], coordinates[-1]
    p1, p2, p3 = control.reshape(3, -1)

    # estimates the curve points by calculating Bézier points for all time values
    estimate = np.array([(1 - t) ** 4 * p0 + 4 * (1 - t) ** 3 * t * p1 + 6 * (1 - t) ** 2 * t ** 2 * p2 + 4 * (
            1 - t) * t ** 3 * p3 + t ** 4 * p4 for t in times])

    # calculates and return the error as sum of squares of the difference between coordinates and estimate
    return np.sum((coordinates - estimate) ** 2)


def fit_quartic_bezier_control_points(coordinates: List[List[float]]) -> np.ndarray:
    """
    Fits a quartic Bézier curve to the given coordinates.

    :param coordinates: A list of touch locations, where each location is a list of x and y coordinates.
    :return: The five control points of a quartic Bézier curve.
    """
    # converts to numpy for numerical calculations
    coordinates_np = np.array(coordinates)
    # creates an array with equally spaced times between 0 and 1 to parametrize the Bézier curve
    times = np.linspace(0, 1, len(coordinates_np))

    # uses the mean of all coordinates as the initial guess for the control points of the Bézier curve
    # the initial guess has five points (hence the repeat)
    initial_guess = np.repeat(coordinates_np.mean(axis=0), 3)

    # uses the BFGS method to minimize the error function and returns the optimal control points that
    # minimizes the difference between the Bézier curve and the given coordinates.
    result = minimize(error_function_quartic, initial_guess, args=(coordinates_np, times), method='BFGS')
    control = result.x.reshape(3, -1)
    return np.array([coordinates_np[0], control[0], control[1], control[2], coordinates_np[-1]])


def generate_two_quartic_beziers_control_points(curve1: List[List[float]], curve2: List[List[float]]) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates two quartic Bézier curves given a list of touch locations.

    :param curve1: The first curve, where each location is a tuple of x and y coordinates.
    :param curve2: The second curve, where each location is a tuple of x and y coordinates.
    :return: Two numpy arrays, each representing a quartic Bézier curve.
    """

    # fits curves into quartic Bézier curves
    curve_points1 = fit_quartic_bezier_control_points(curve1)
    curve_points2 = fit_quartic_bezier_control_points(curve2)

    return curve_points1, curve_points2


def calculate_quartic_bezier_curve_point(t: float, control_points: np.ndarray) -> np.ndarray:
    """
    Calculates the point on the quartic Bézier curve at the given parameter t.

    :param t: The parameter at which to calculate the point.
    :param control_points: The five control points of the quartic Bézier curve.
    :return: The point on the Bézier curve at the given parameter.
    """
    assert 0 <= t <= 1, "Parameter t must be between 0 and 1."

    P0, P1, P2, P3, P4 = control_points
    B_t = ((1 - t) ** 4) * P0 + 4 * ((1 - t) ** 3) * t * P1 + 6 * ((1 - t) ** 2) * (t ** 2) * P2 + 4 * (1 - t) * (
            t ** 3) * P3 + (t ** 4) * P4
    return B_t


def return_quartic_bezier_curve(control_points: np.ndarray, num_points: int = 100) -> np.ndarray:
    """
    Generates points on the quartic Bézier curve described by the given control points.

    :param control_points: The five control points of the quartic Bézier curve.
    :param num_points: The number of points to generate on the curve.
    :return: A numpy array of points on the Bézier curve.
    """
    t_values = np.linspace(0, 1, num_points)
    curve_points = np.array([calculate_quartic_bezier_curve_point(t, control_points) for t in t_values])
    return curve_points


def return_two_quartic_bezier_curves(bezier1_control: np.ndarray, bezier2_control: np.ndarray) -> \
        Tuple[np.ndarray, np.ndarray]:
    """
    Generates two quartic Bézier curves given the control points for each curve.

    :param bezier1_control: The control points for the first quartic Bézier curve, in a numpy array.
    :param bezier2_control: The control points for the second quartic Bézier curve, in a numpy array.
    :return: A tuple of two numpy arrays, each representing a quartic Bézier curve.
    """
    bezier1_curve = return_quartic_bezier_curve(bezier1_control)
    bezier2_curve = return_quartic_bezier_curve(bezier2_control)
    return bezier1_curve, bezier2_curve
