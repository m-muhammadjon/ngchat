from .base import *  # noqa

CELERY_TASK_ALWAYS_EAGER = True

MIDDLEWARE += [  # noqa F405
    "querycount.middleware.QueryCountMiddleware",
]
QUERYCOUNT = {
    "THRESHOLDS": {"MEDIUM": 50, "HIGH": 200, "MIN_TIME_TO_LOG": 0, "MIN_QUERY_COUNT_TO_LOG": 0},
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": None,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}
