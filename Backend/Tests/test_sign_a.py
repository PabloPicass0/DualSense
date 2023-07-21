import pytest
from sign_a.sign_a import *


def test_location_inside_circle():
    assert locations_inside_circle([[477.5, 755.5], [477.5, 386.0], [847.0, 755.5]]) == True
    assert locations_inside_circle([[477.5, 755.5], [477.5, 1000.0], [1000.0, 755.5]]) == False


def test_is_sign_a():
    assert is_sign_a([0.0, 1.0, 2.0], [[477.5, 755.5], [477.5, 386.0], [847.0, 755.5]]) == True
    assert is_sign_a([0.0, 2.0, 5.0], [[477.5, 755.5], [477.5, 1000.0], [1000.0, 755.5]]) == False


if __name__ == '__main__':
    pytest.main()
