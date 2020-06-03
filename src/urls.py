from django.conf.urls import url
from django.urls import include, path

from .index import view as index

urlpatterns = [
    path("", index),
    url("-/", include("django_prometheus.urls")),
    url("-/", include("src.health_check.urls")),
]
