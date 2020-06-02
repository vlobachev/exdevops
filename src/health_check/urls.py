from django.urls import re_path

from . import views

urlpatterns = [re_path(r"ping/?", views.ping, name="ping"), re_path(r"status/?", views.status, name="status")]
