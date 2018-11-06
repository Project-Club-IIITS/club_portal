from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestBlankUrl(TestCase):
    def setUp(self):
        self.request_url = ''

        self.client = None
        # Create clients on the fly in each func
        self.created_user = User.objects.create(username="testuser", email="sampleuser@testusers.com",
                                                password="who cares?")

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.created_user)

        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
