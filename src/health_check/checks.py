import sys

from django_redis.cache import RedisCache

from django.core.cache import caches
from django.db import Error as AnyDBRelatedError
from django.db import connection

from .. import __version__

TEST_KEY = "status"
TEST_VALUE = "TEST"
cache = caches["default"]  # pylint: disable=invalid-name


def db_connection() -> str:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        return ""
    except AnyDBRelatedError:
        return "error at db communication"


def cache_execution() -> str:
    try:
        cache.set(TEST_KEY, TEST_VALUE, 5)
        if cache.get(TEST_KEY) != TEST_VALUE:
            return "cache unhealthy"
    except Exception as exc:  # pylint: disable=broad-except
        return f"error on cache set/get {exc}"
    return ""


def db_vendor():
    if connection.vendor != "postgresql":
        return f"wrong db vendor {connection.vendor} != postgresql"
    return None


def cache_class():
    if not isinstance(cache, RedisCache):
        return "cache wrong class"
    return None


def python_version():
    if sys.version_info.major != 3 or sys.version_info.minor != 8:
        return "python wrong version (should be 3.8)"
    return None


def version():
    if not __version__:
        return "app version should be defined"
    return None
