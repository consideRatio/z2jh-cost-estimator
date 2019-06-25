import pytest
import numpy as np

from ..generate_user_activity import generate_user_activity


def test_no_users():
    # the activity of multiple users, for two hours
    hour_wise_simultaneous_users = [2, 3]

    user_activities = generate_user_activity(hour_wise_simultaneous_users)

    number_of_users_active_in_the_first_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[0:60]) == 60
        ]
    )
    assert number_of_users_active_in_the_first_hour == 2

    number_of_users_active_in_the_second_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[60:120]) == 60
        ]
    )
    assert number_of_users_active_in_the_second_hour == 3


def test_decrease_of_no_of_users():
    # the activity of multiple users, for fourhours
    hour_wise_simultaneous_users = [2, 3, 4, 2]
    user_activities = generate_user_activity(hour_wise_simultaneous_users)

    number_of_users_active_in_the_first_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[0:60]) == 60
        ]
    )
    assert number_of_users_active_in_the_first_hour == 2

    number_of_users_active_in_the_third_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[120:180]) == 60
        ]
    )
    assert number_of_users_active_in_the_third_hour == 4

    number_of_users_active_in_the_fourth_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[180:240]) == 60
        ]
    )
    assert number_of_users_active_in_the_fourth_hour == 2


def test_same_no_of_users():
    # the activity of multiple users, forfour hours
    hour_wise_simultaneous_users = [2, 3, 4, 4]

    user_activities = generate_user_activity(hour_wise_simultaneous_users)

    number_of_users_active_in_the_first_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[0:60]) == 60
        ]
    )
    assert number_of_users_active_in_the_first_hour == 2

    number_of_users_active_in_the_third_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[120:180]) == 60
        ]
    )
    assert number_of_users_active_in_the_third_hour == 4

    number_of_users_active_in_the_fourth_hour = len(
        [
            user_activity
            for user_activity in user_activities
            if np.sum(user_activity[180:240]) == 60
        ]
    )
    assert number_of_users_active_in_the_fourth_hour == 4
