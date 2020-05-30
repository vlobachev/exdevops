from django.db import models


class SomethingBad(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    what = models.CharField(max_length=255)
