from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url("-/", include("django_prometheus.urls")),
    url("-/", include("src.health_check.urls")),
]
