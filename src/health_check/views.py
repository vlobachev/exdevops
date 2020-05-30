import sys

from django import db
from django.http import JsonResponse

from .. import __version__
from .models import SomethingBad
from .utils import get_cache_error, get_db_connection_error


def check_db():
    if db.connection.vendor != "postgresql":
        return f"wrong db vendor {db.connection.vendor} != postgresql"
    return None


def check_python_version():
    if sys.version_info.major != 3 or sys.version_info.minor != 8:
        return "python wrong version (should be 3.8)"
    return None


CHECKS = (get_db_connection_error, get_cache_error, check_db, check_python_version)


def ping(request):
    return JsonResponse(data={"status": "ok"}, status=200)


def status(request):
    errors = []
    db_error = False
    for check_number, check in enumerate(CHECKS):
        _error = check()
        if not _error:
            continue
        errors.append(_error)
        if check_number == 0:
            db_error = True
    if not db_error and errors:
        SomethingBad.objects.create(what="; ".join(errors))
    data = {"version": __version__, "status": bool(errors), "errors": errors}
    return JsonResponse(data=data, status=200 if not errors else 500)
