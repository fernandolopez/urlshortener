from django.contrib import admin
from . import models


class UrlAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(models.Url, UrlAdmin)
