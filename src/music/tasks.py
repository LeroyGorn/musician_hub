import random
import time

from celery import shared_task
from django.contrib.auth import get_user_model
from faker import Faker

from accounts.models import ForumUser
from music.models import ForumCategory, ForumComments


@shared_task
def mine_bitcoin():
    time.sleep(random.randint(1, 10))


@shared_task
def normalize_email_task(filter):
    query_set = ForumUser.objects.filter(**filter)
    if query_set:
        for user in query_set:
            print("working with user: {user.email}")
            user.save()
    else:
        print("Empty data")


fake = Faker()


@shared_task
def fake_data(number):
    for i in range(0, number):
        fake_name = fake.name()
        fake_desc = fake.sentence(nb_words=70)
        cat_item = ForumCategory.objects.get_or_create(name=fake_name, description=fake_desc)
        cat_item.save()

    for i in range(0, number):
        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()
        fake_email = fake.email()
        user_item = ForumUser.objects.get_or_create(
            email=fake_email, first_name=fake_first_name, last_name=fake_last_name
        )
        user_item.set_password("12345")
        user_item.save()

    for i in range(0, number):
        fake_uuid = fake.UUID.v4()
        fake_desc = fake.sentence(nb_words=70)
        comments_item = ForumComments.objects.get_or_create(
            author=get_user_model(), messages=fake_uuid, text=fake_desc
        )
        comments_item.save()
