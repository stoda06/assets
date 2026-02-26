import logging

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template.loader import render_to_string
from django.urls.exceptions import Resolver404

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    Middleware that catches unhandled exceptions and returns clean error pages.

    Prevents Django's default debug 404 handler from causing cascading
    VariableDoesNotExist exceptions when iterating URLResolver objects
    that lack a 'name' attribute.

    Add to MIDDLEWARE in settings.py:
        'assets.middleware.ErrorHandlerMiddleware'
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Resolver404):
            logger.warning("Not Found: %s", request.path)
            html = render_to_string('404.html', request=request)
            return HttpResponseNotFound(html)

        logger.exception("Internal Server Error: %s", request.path)
        html = render_to_string('500.html')
        return HttpResponseServerError(html)
