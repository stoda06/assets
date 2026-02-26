import logging
import re

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import Resolver404

logger = logging.getLogger(__name__)


class LoginRequiredMiddleware:
    """
    Middleware that redirects unauthenticated users to the login page.

    Exempts URLs matching patterns in settings.LOGIN_EXEMPT_URLS
    and the login URL itself.

    Add to MIDDLEWARE in settings.py (after AuthenticationMiddleware):
        'assets.middleware.LoginRequiredMiddleware'
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')

            # Don't redirect the login URL itself or admin login
            exempt_paths = [login_url, '/admin/login/']

            # Add any exempt URLs from settings
            exempt_patterns = getattr(settings, 'LOGIN_EXEMPT_URLS', [])
            for pattern in exempt_patterns:
                if re.match(pattern, request.path_info.lstrip('/')):
                    return self.get_response(request)

            if request.path_info not in exempt_paths:
                return redirect(f'{login_url}?next={request.path_info}')

        return self.get_response(request)


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
