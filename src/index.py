from functools import lru_cache

from markdown import markdown

from django.conf import settings
from django.http import HttpResponse


@lru_cache()
def readme_in_html():
    with open(settings.README_PATH, "r") as readme:
        return markdown(readme.read())


def view(request):
    return HttpResponse(content=readme_in_html())
