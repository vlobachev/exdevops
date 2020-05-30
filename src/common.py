import json
import logging
import time

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        logger.info("start request", extra={"path": request.path})
        response = self.get_response(request)
        logger.info(
            "finish request",
            extra={"path": request.path, "status": response.status_code, "spent": time.perf_counter() - start},
        )
        return response


class JsonFormatter(logging.Formatter):
    def __init__(self, fields=(), **kwargs):
        self._fields = fields
        super().__init__(**kwargs)

    def formatMessage(self, record: logging.LogRecord) -> str:
        msg = super().formatMessage(record)
        data = {"message": msg, "level": record.levelname, "path": record.pathname}
        for field in self._fields:
            data[field] = getattr(record, field, None)
        return json.dumps(data)
