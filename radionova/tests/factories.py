from datetime import timedelta, timezone
from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from radionova.models import Post

faker = Factory.create()


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    body = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    created = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    updated = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    heading = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
