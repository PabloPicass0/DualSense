import json
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from extraction import extract_timestamps_and_locations
from scipy.optimize import minimize

from recognition import compare_sequences
from sign_a import timestamp_duration_valid

""" The functions for the quadratic curve are not implemented, but have been tried. The cubic curve 
    showed more flexibility. """


def calculate_bezier_point_quadratic(t: float, p0: np.array, p1: np.array, p2: np.array) -> np.array:
    """
    Calculate a point on a quadratic Bézier curve.

    :param t: The t-value at which to evaluate the curve (0 <= t <= 1).
    :param p0: The first point defining the Bézier curve.
    :param p1: The control point defining the curve.
    :param p2: The last point defining the Bézier curve.
    :return: The calculated point on the curve.
    """
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2


def error_function_quadratic(control: np.array, coordinates: np.ndarray, times: np.ndarray) -> np.array:
    """
    Error function for the optimization problem. The error is the sum of squares of the differences
    between the coordinates and the estimated points on the curve.

    :param control: Control point for Bézier curve.
    :param coordinates: Coordinates through which the curve should pass.
    :param times: Array of equally spaced time instances.
    :return: The calculated error.
    """
    p0, p2 = coordinates[0], coordinates[-1]
    p1 = np.array(control)
    estimate = np.array([calculate_bezier_point_quadratic(t, p0, p1, p2) for t in times])
    return np.sum((coordinates - estimate).flatten() ** 2)


def fit_quadratic_bezier_curve(coordinates: List[List[float]]) -> np.ndarray:
    """
    Fit a quadratic Bézier curve to the given coordinates.

    :param coordinates: The coordinates through which the curve should pass.
    :return: The control points for the fitted Bézier curve as a np.ndarray.
    """
    # converts coordinates to numpy array for processing
    coordinates_np = np.array(coordinates)

    times = np.linspace(0, 1, len(coordinates_np))
    initial_guess = coordinates_np.mean(axis=0)
    result = minimize(error_function_quadratic, initial_guess, args=(coordinates_np, times), method='BFGS')
    control = result.x

    # packages results as a np.ndarray
    return np.array([coordinates_np[0], control, coordinates_np[-1]])


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


def fit_bezier_for_j():
    """
    This function fits a cubic Bézier curve to the given data and saves it as a template for later comparison.
    Used only once for saving templates of the sign.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_j.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_j = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_j)

    curve_points = return_cubic_bezier(locations)

    # converts list of tuples to numpy array
    curve_points_np = np.array(curve_points)

    # saves the template for future use
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    np.save(file_path_b, curve_points_np)

    # plots curves
    plt.plot(curve_points_np[:, 0], curve_points_np[:, 1], color='blue')

    plt.show()


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


def is_sign_j(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "J"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # creates cubic Bézier curve representing the user-performed gesture
    curve_points_user = return_cubic_bezier(locations)

    # loads the template for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b = os.path.join(current_dir, 'bezier_curve_template.npy')
    bezier_curve_template = np.load(file_path_b)

    # converts list of numpy arrays to a single 2D numpy array
    curve_points_user = np.vstack(curve_points_user)
    bezier_curve_template = np.vstack(bezier_curve_template)

    # calculates distance using DTW
    distance_template = compare_sequences(curve_points_user, bezier_curve_template)

    # debugging
    print(f"distance_template: {distance_template}")

    # compares if distance to template is below threshold
    if distance_template > 3000.0:
        return False

    # checks if time frame is valid
    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    return True


if __name__ == '__main__':
    fit_bezier_for_j()
