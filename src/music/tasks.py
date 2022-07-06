import json
import random
import time

import numpy as np
from celery import shared_task
from faker import Faker


@shared_task
def mine_bitcoin():
    time.sleep(random.randint(1, 10))


@shared_task
def normalize_email_task(query_set):

    if query_set:
        for user in query_set:
            print("working with user: {user.email}")
            user.save()
    else:
        print("Empty data")


fake = Faker()


@shared_task
def fake_data(number):
    friends_data = {}
    for i in range(0, number):
        friends_data[i] = {}
        friends_data[i]["name"] = fake.name()
        friends_data[i]["address"] = fake.address()
        friends_data[i]["city"] = fake.city()
        friends_data[i]["color"] = fake.color()
        friends_data[i]["closeness (1-5)"] = np.random.randint(0, 5)

    return friends_data
