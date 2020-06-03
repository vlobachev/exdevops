from django.http import JsonResponse

from .. import __version__
from . import checks
from .models import SomethingBad

CHECKS = (
    checks.db_connection,
    checks.cache_execution,
    checks.db_vendor,
    checks.cache_class,
    checks.python_version,
    checks.version,
    checks.user_privileges,
)


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
    data = {"version": __version__, "status": not bool(errors), "errors": errors}
    return JsonResponse(data=data, status=200 if not errors else 500)
