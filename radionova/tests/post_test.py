import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Post
from .factories import PostFactory

faker = Factory.create()


class Post_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        PostFactory.create_batch(size=3)

    def test_create_post(self):
        """
        Ensure we can create a new post object.
        """
        client = self.api_client
        post_count = Post.objects.count()
        post_dict = factory.build(dict, FACTORY_CLASS=PostFactory)
        response = client.post(reverse('post-list'), post_dict)
        created_post_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == post_count + 1
        post = Post.objects.get(pk=created_post_pk)

        assert post_dict['body'] == post.body
        assert post_dict['created'] == post.created.isoformat()
        assert post_dict['updated'] == post.updated.isoformat()
        assert post_dict['heading'] == post.heading

    def test_get_one(self):
        client = self.api_client
        post_pk = Post.objects.first().pk
        post_detail_url = reverse('post-detail', kwargs={'pk': post_pk})
        response = client.get(post_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('post-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Post.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        post_qs = Post.objects.all()
        post_count = Post.objects.count()

        for i, post in enumerate(post_qs, start=1):
            response = client.delete(reverse('post-detail', kwargs={'pk': post.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert post_count - i == Post.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        post_pk = Post.objects.first().pk
        post_detail_url = reverse('post-detail', kwargs={'pk': post_pk})
        post_dict = factory.build(dict, FACTORY_CLASS=PostFactory)
        response = client.patch(post_detail_url, data=post_dict)
        assert response.status_code == status.HTTP_200_OK

        assert post_dict['body'] == response.data['body']
        assert post_dict['created'] == response.data['created'].replace('Z', '+00:00')
        assert post_dict['updated'] == response.data['updated'].replace('Z', '+00:00')
        assert post_dict['heading'] == response.data['heading']

    def test_update_created_with_incorrect_value_data_type(self):
        client = self.api_client
        post = Post.objects.first()
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        post_created = post.created
        data = {
            'created': faker.pystr(),
        }
        response = client.patch(post_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert post_created == Post.objects.first().created

    def test_update_updated_with_incorrect_value_data_type(self):
        client = self.api_client
        post = Post.objects.first()
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        post_updated = post.updated
        data = {
            'updated': faker.pystr(),
        }
        response = client.patch(post_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert post_updated == Post.objects.first().updated

    def test_update_body_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        post = Post.objects.first()
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        post_body = post.body
        data = {
            'body': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(post_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert post_body == Post.objects.first().body

    def test_update_heading_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        post = Post.objects.first()
        post_detail_url = reverse('post-detail', kwargs={'pk': post.pk})
        post_heading = post.heading
        data = {
            'heading': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(post_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert post_heading == Post.objects.first().heading
