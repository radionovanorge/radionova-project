from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from radionova.serializers import PostSerializer

from .factories import PostFactory


class PostSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = PostFactory.create()

    def test_that_a_post_is_correctly_serialized(self):
        post = self.post
        serializer = PostSerializer
        serialized_post = serializer(post).data

        assert serialized_post['id'] == post.id
        assert serialized_post['body'] == post.body
        assert serialized_post['created'] == post.created
        assert serialized_post['updated'] == post.updated
        assert serialized_post['heading'] == post.heading
