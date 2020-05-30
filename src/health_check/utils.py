from django.core.cache import cache
from django.db import Error as AnyDBRelatedError
from django.db import connection

TEST_KEY = "status"
TEST_VALUE = "TEST"


def get_db_connection_error() -> str:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        return ""
    except AnyDBRelatedError:
        return "error at db communication"


def get_cache_error() -> str:
    try:
        cache.set(TEST_KEY, TEST_VALUE, 5)
        if cache.get(TEST_KEY) != TEST_VALUE:
            return "cache unhealthy"
    except Exception:  # pylint: disable=broad-except
        return "error on cache set/get"
    return ""
