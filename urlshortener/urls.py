"""
URL configuration for urlshortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shortener.views import HandleUrls, slug_redirect_handler

api_router = routers.DefaultRouter()
api_router.register("url", HandleUrls)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_router.urls)),
    path("g/<slug:slug>", slug_redirect_handler)
]
