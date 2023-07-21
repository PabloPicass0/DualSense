import pytest

from sign_b.sign_b import *


def test_locations_inside_rectangle():
    assert locations_inside_rectangle([[200.0, 600.0], [300.0, 700.0]])  # all points inside the rectangle
    assert not locations_inside_rectangle([[200.0, 600.0], [1000.0, 1100.0]])  # one point outside the rectangle


def test_is_sign_b():
    # valid sign B
    assert is_sign_b([1.0, 2.0, 3.0], [[200.0, 600.0], [300.0, 700.0], [400.0, 800.0]])
    # invalid sign B (one point outside the rectangle)
    assert not is_sign_b([1.0, 2.0, 3.0], [[200.0, 600.0], [300.0, 700.0], [1000.0, 1100.0]])
    # invalid sign B (too many touch points)
    assert not is_sign_b([1.0, 2.0, 3.0] * 10, [[200.0, 600.0], [300.0, 700.0], [400.0, 800.0]] * 10)
    # invalid sign B (duration too long)
    assert not is_sign_b(list(range(1, 6, 4)), [[200.0, 600.0], [300.0, 700.0], [400.0, 800.0]])


if __name__ == '__main__':
    pytest.main()
