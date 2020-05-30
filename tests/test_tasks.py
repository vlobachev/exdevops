import pytest

from src.health_check.models import SomethingBad

pytestmark = pytest.mark.django_db


def test_update_user_tasks():
    assert SomethingBad.objects.all().count() == 0
    SomethingBad.objects.create(what="test")
    assert SomethingBad.objects.all().count() == 1
