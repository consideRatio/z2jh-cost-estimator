import pytest
import numpy as np

from ..generate_user_activity import generate_user_activity


def test_pytest_setup():
    """Dummy test to verify we can run tests at all."""
    hour_wise_users = [2, 3]
    user_activity = generate_user_activity(hour_wise_users)
    list1 = [user for user in user_activity if np.sum(user[0:60]) == 60]
    assert len(list1) == 2
    list2 = [user for user in user_activity if np.sum(user[60:120]) == 60]
    assert len(list2) == 3


def test_no_users():
    """Dummy test to verify we can run tests at all."""
    hour_wise_users = [2, 3, 4, 2]
    user_activity = generate_user_activity(hour_wise_users)
    list1 = [user for user in user_activity if np.sum(user[120:180]) == 60]
    assert len(list1) == 4
    list2 = [user for user in user_activity if np.sum(user[180:240]) == 60]
    assert len(list2) == 2


def test_same_no_users():
    """Dummy test to verify we can run tests at all."""
    hour_wise_users = [2, 3, 4, 4]
    user_activity = generate_user_activity(hour_wise_users)
    list1 = [user for user in user_activity if np.sum(user[0:60]) == 60]
    assert len(list1) == 2
    list2 = [user for user in user_activity if np.sum(user[120:180]) == 60]
    assert len(list2) == 4

    list3 = [user for user in user_activity if np.sum(user[180:240]) == 60]
    assert len(list3) == 4
