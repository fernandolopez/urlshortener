import re
from .models import Url, MAX_URL_LEN
from string import ascii_letters, digits
from random import choice
from dotenv import load_dotenv
from os import getenv
from threading import Thread
import requests
import bs4
from django.db import transaction

load_dotenv()

VALID_URL_RE = re.compile(r"https?://.+")
SLUG_CHARS = ascii_letters + digits
SLUG_SIZE = int(getenv("SLUG_SIZE"))
SLUG_COLISION_RETRIES = int(getenv("SLUG_COLISION_RETRIES"))

class UrlServiceError(Exception):
    """Base class for URL shortener service exceptions"""

class InvalidURLError(UrlServiceError):
    """Original URL doesn't have a valid format"""


class URLTooLongError(UrlServiceError):
    """URL is too long to store in current implementation"""


class SlugsDepletedError(UrlServiceError):
    """Not enought slugs with current configuration, increase slug size"""


def random_sequence(chars):
    return "".join([choice(SLUG_CHARS) for _ in range(chars)])


def t_retrieve_title(url_id, original_url):
    try:
        content = requests.get(original_url).text
        title = bs4.BeautifulSoup(content, features="html.parser").title.string
    except Exception:
        pass
    else:
        url = Url.objects.get(id=url_id)
        url.title = title
        url.save()


def retrieve_title(url_id, original_url):
    Thread(target=t_retrieve_title, args=[url_id, original_url]).start()


def create_url(original_url):
    if not original_url:  # FIXME or VALID_URL_RE.fullmatch(original_url):
        raise InvalidURLError()
    elif len(original_url) > MAX_URL_LEN:
        raise URLTooLongError()

    for _ in range(SLUG_COLISION_RETRIES):
        slug = random_sequence(SLUG_SIZE)
        if not Url.objects.filter(slug=slug).exists():
            break
    else:
        raise SlugsDepletedError()

    url = Url.objects.create(url=original_url, slug=slug)
    transaction.on_commit(lambda: retrieve_title(url.id, original_url))
    
    return url
