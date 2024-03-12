from django.test import TestCase
from unittest import mock
from .models import Url
from .services import create_url, random_sequence


# Create your tests here.
class TestCreateUrl(TestCase):
    def test_create_empty_url(self):
        with self.assertRaises(Exception):
            create_url("")

    def test_create_shortened_valid_url(self):
        create_url("http://www.example.com")
        self.assertTrue(Url.objects.all(), "At least shorted url created")
        self.assertTrue(Url.objects.first().slug, "Slug is not empty")

    def test_check_for_repeated_slugs(self):
        Url.objects.create(url="http://foo.com", slug="aaaaa")
        with mock.patch(
            "shortener.services.random_sequence", side_effect=["aaaaa", "bbbbb"]
        ):
            create_url("http://bar.com")

        Url.objects.filter(url="http://bar.com").first().slug == "bbbbb"


class TestRandomSequence(TestCase):
    def test_random_sequence_returns_valid_len_string(self):
        self.assertTrue(len(random_sequence(5)) == 5)
