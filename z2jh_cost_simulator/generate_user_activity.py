import random
import numpy as np


def generate_user_activity(simultaneous_user_count):
    """Takes a list of integers representing the number of simultaenous users and provides a list of users and their 'user_activity'."""
    user_pool = []
    hour_wise_users = simultaneous_user_count
    count_users = 0

    for index in range(len(hour_wise_users)):

        if count_users == hour_wise_users[index]:
            for user_activity in random.sample(user_pool, k=hour_wise_users[index]):
                _scale_user_activity(user_activity, index)

        else:
            if hour_wise_users[index] > count_users:
                for user_activity in random.sample(user_pool, k=count_users):
                    _scale_user_activity(user_activity, index)

                for count in range(
                    hour_wise_users[index] - count_users
                ):  # adding the users.
                    user_activity = np.zeros(len(hour_wise_users) * 60)
                    user_activity = _scale_user_activity(user_activity, index)
                    user_pool.append(user_activity)
                    count_users = count_users + 1
            else:
                for user_activity in random.sample(user_pool, k=hour_wise_users[index]):
                    _scale_user_activity(user_activity, index)
    return user_pool


def _scale_user_activity(user_activity, index, scale=60):
    """This helper function expects a user_activity list and will return it but with many more elements. For example, you could transition from a hour resolution to a minute resolution by scaling with 60."""
    user_activity[index * scale : (index + 1) * scale] = 1
    return user_activity
