import json
import os
from typing import List, Tuple

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from scipy.spatial.distance import euclidean
from extraction import extract_timestamps_and_locations
from sign_ch.sign_ch import compare_sequences

matplotlib.use('Agg')


def split_touch_locations(locations: List[List[float]]) -> Tuple[
    List[List[float]], List[List[float]]]:
    """
    Splits the provided locations into two curves based on a distance threshold. Needs a higher distance threshold as
    the function for sign ch as a few points of the same curve have been further apart and were mistakenly assigned to
    curve2.

    :param locations: A list of tuples, each representing the (x, y) coordinates of a point.

    :return: Two lists of tuples, each list represents a curve and each tuple within the list represents a point on the
    curve.
    """
    curve1 = []
    curve2 = []

    # starts by putting the first point in curve1
    curve1.append(locations[0])
    for i in range(1, len(locations)):
        # assigns point to either curve1 or curve2 depending on distance
        if euclidean(locations[i], curve1[-1]) <= 100:
            curve1.append(locations[i])
        else:
            curve2.append(locations[i])

    return curve1, curve2


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


def generate_two_quartic_beziers_control_points(locations: List[List[float]]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates two quartic Bézier curves given a list of touch locations.

    :param locations: The list of touch locations, where each location is a tuple of x and y coordinates.
    :return: Two numpy arrays, each representing a quartic Bézier curve.
    """
    # splits touch locations into individual curves
    curve1, curve2 = split_touch_locations(locations)

    # raises error if curve2 is empty
    if not curve2:
        raise ValueError("Curve2 is empty.")

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


def fit_bezier_for_ll():
    """
    This function fits two quartic Bézier curves to the given data and saves them as templates for later comparison.
    Used only once for saving templates of the sign ll.
    """
    # defines filepath; function needs to be run from root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data_ll.json')

    # opens and loads the JSON file
    with open(file_path) as file:
        data_ll = json.load(file)

    # splits data into touch locations and timestamps
    timestamps, locations = extract_timestamps_and_locations(data_ll)

    # generates Bezier curve control points
    bezier1_control, bezier2_control = generate_two_quartic_beziers_control_points(locations)

    # calculates and returns full curves
    bezier1_curve, bezier2_curve = return_two_quartic_bezier_curves(bezier1_control, bezier2_control)

    # transforms into numpy arrays
    bezier1_curve_np = np.array(bezier1_curve)
    bezier2_curve_np = np.array(bezier2_curve)

    # plots the first Bézier curve
    plt.figure(figsize=(6, 6))
    plt.plot(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], label='Bezier 1')
    plt.scatter(bezier1_curve_np[:, 0], bezier1_curve_np[:, 1], s=10)

    # plots the second Bézier curve
    plt.plot(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], label='Bezier 2')
    plt.scatter(bezier2_curve_np[:, 0], bezier2_curve_np[:, 1], s=10)

    # setting up the title and labels
    plt.title('Bezier Curves')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # displays the legend
    plt.legend()

    # shows the plot
    plt.show()

    # saves the templates for future use
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    np.save(file_path_b1, bezier1_curve)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    np.save(file_path_b2, bezier2_curve)


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


def timestamp_duration_valid(timestamps: List[float]) -> bool:
    """
    Checks whether the difference between the first and the last timestamp is larger than 4 seconds. Sign LL may take
    longer than other signs and therefore has a longer time frame than other signs.

    :param timestamps: List of timestamps
    :return: True if the duration is less than or equal to 3 seconds, False otherwise
    """
    return timestamps[-1] - timestamps[0] <= 4


def is_sign_ll(timestamps: List[float], locations: List[List[float]]) -> bool:
    """
    This function takes a list of timestamps and a list of touch locations as input.
    It checks whether the gesture represented by these data points matches the gesture of "LL"
    according to a predefined template of the gesture.
    If the performed gesture deviates from the template by more than a certain threshold,
    the function returns False. Otherwise, it returns True.

    :param timestamps: A list of timestamps.
    :param locations: A list of touch locations, where each location is a list of x and y coordinates.
    :return: True if the gesture matches the template, False otherwise.
    """
    # checks if time frame is valid
    if not timestamp_duration_valid(timestamps):
        print("Duration too long")
        return False

    try:
        # splits location points into respective curves and returns control points
        user_curve_1_control, user_curve_2_control = generate_two_quartic_beziers_control_points(locations)
    except ValueError:
        print("\nCurve2 is empty")
        return False

    # creates full Bezier curves
    user_curve_1_b, user_curve_2_b = return_two_quartic_bezier_curves(user_curve_1_control, user_curve_2_control)

    # loads the templates for comparison
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_b1 = os.path.join(current_dir, 'bezier1_upper_curve_template.npy')
    bezier1_upper_curve_template = np.load(file_path_b1)
    file_path_b2 = os.path.join(current_dir, 'bezier2_lower_curve_template.npy')
    bezier2_lower_curve_template = np.load(file_path_b2)

    # # The code below saves a figure to see how the user curves compare to the templates
    # # Needs to uncomment agg at the top of the file
    # creates a new figure
    # plt.figure()
    # # plots the templates
    # plt.plot(bezier1_upper_curve_template[:, 0], bezier1_upper_curve_template[:, 1], label='Bezier 1 Template',
    #          linestyle='dashed')
    # plt.plot(bezier2_lower_curve_template[:, 0], bezier2_lower_curve_template[:, 1], label='Bezier 2 Template',
    #          linestyle='dashed')
    # # plots user curves
    # plt.plot(user_curve_1_b[:, 0], user_curve_1_b[:, 1], label='User Bezier 1')
    # plt.plot(user_curve_2_b[:, 0], user_curve_2_b[:, 1], label='User Bezier 2')
    # # adds a legend
    # plt.legend()
    # # saves the plot
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # filename = os.path.join(current_dir, 'output_figure.png')
    # plt.savefig(filename)
    # # closes the figure to free up memory
    # plt.close()

    # calculates the Euclidean distance between the first point of user's curves and the first point of the templates
    dist1 = euclidean(user_curve_1_b[0], bezier1_upper_curve_template[0])
    dist2 = euclidean(user_curve_1_b[0], bezier2_lower_curve_template[0])

    if dist1 < dist2:
        # if the first point of user_curve_1 is closer to bezier1
        distance1_template = compare_sequences(user_curve_1_b, bezier1_upper_curve_template)
        distance2_template = compare_sequences(user_curve_2_b, bezier2_lower_curve_template)
    else:
        # if the first point of user_curve_1 is closer to bezier2
        distance1_template = compare_sequences(user_curve_1_b, bezier2_lower_curve_template)
        distance2_template = compare_sequences(user_curve_2_b, bezier1_upper_curve_template)

    print(f"distance1_template: {distance1_template}")
    print(f"distance2_template: {distance2_template}")

    if distance1_template > 5000.0 or distance2_template > 5500.0:
        return False

    return True


if __name__ == '__main__':
    fit_bezier_for_ll()
