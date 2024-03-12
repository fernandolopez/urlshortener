from django.db import models

MAX_URL_LEN = 4096

# Create your models here.
class Url(models.Model):
    class Meta:
        indexes = [models.Index(fields=["slug"])]

    url = models.CharField(max_length=MAX_URL_LEN)
    slug = models.CharField(max_length=512, unique=True)
    visit_count = models.IntegerField(default=0)
    title = models.CharField(max_length=1024, null=True, blank=True)
