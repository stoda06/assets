import logging
import re

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls.exceptions import Resolver404

logger = logging.getLogger(__name__)


class LoginRequiredMiddleware:
    """
    Middleware that redirects unauthenticated users to the login page
    and serves the login form directly (independent of URL routing).

    Add to MIDDLEWARE in settings.py (after AuthenticationMiddleware):
        'assets.middleware.LoginRequiredMiddleware'
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        user = getattr(request, 'user', None)

        # Serve the login page directly from middleware
        if request.path_info == login_url:
            if user and user.is_authenticated:
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            if request.method == 'POST':
                return self._handle_login_post(request, login_url)
            return self._render_login(request)

        if not request.user.is_authenticated:
            # Don't redirect admin login or unauthenticated API endpoints
            exempt_prefixes = ['/admin/login/', '/systeminfo']

            # Add any exempt URLs from settings
            exempt_patterns = getattr(settings, 'LOGIN_EXEMPT_URLS', [])
            for pattern in exempt_patterns:
                if re.match(pattern, request.path_info.lstrip('/')):
                    return self.get_response(request)

            if not any(request.path_info.startswith(p) for p in exempt_prefixes):
                return redirect(f'{login_url}?next={request.path_info}')

        return self.get_response(request)

    def _handle_login_post(self, request, login_url):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        remote_addr = request.META.get('REMOTE_ADDR', 'unknown')
        logger.info("Login attempt for user=%r from %s", username, remote_addr)
        try:
            user = authenticate(request, username=username, password=password)
        except Exception:
            logger.exception(
                "Authentication error for user=%r from %s", username, remote_addr,
            )
            return self._render_login(
                request,
                error="Unable to contact Active Directory. Please try again later or contact IT.",
            )
        if user is not None:
            backend_used = getattr(user, 'backend', '')
            if backend_used != 'django_auth_ldap.backend.LDAPBackend':
                logger.warning(
                    "User %r authenticated via %s instead of LDAP from %s",
                    username, backend_used, remote_addr,
                )
                return self._render_login(
                    request,
                    error="Authentication must use Active Directory. Local database login is not permitted.",
                )
            try:
                login(request, user)
            except AttributeError:
                logger.exception(
                    "Session not available during login for user=%r from %s — "
                    "check MIDDLEWARE order (SessionMiddleware must precede "
                    "LoginRequiredMiddleware)",
                    username, remote_addr,
                )
                return self._render_login(
                    request,
                    error="Login failed due to a server configuration error. Please contact IT.",
                )
            except Exception:
                logger.exception(
                    "Unexpected error during login for user=%r from %s",
                    username, remote_addr,
                )
                return self._render_login(
                    request,
                    error="An unexpected error occurred during login. Please try again.",
                )
            logger.info("Login successful for user=%r via LDAP from %s", username, remote_addr)
            return redirect(next_url)
        logger.warning(
            "Login failed for user=%r from %s (authenticate returned None)",
            username, remote_addr,
        )
        return self._render_login(request, error="Invalid username or password.")

    def _render_login(self, request, error=False):
        get_token(request)
        try:
            html = render_to_string(
                'registration/login.html',
                {'error': error, 'next': request.GET.get('next', '/')},
                request=request,
            )
        except Exception:
            logger.exception("Failed to render login template")
            csrf_token = get_token(request)
            error_html = f'<div style="color:red">{error}</div>' if error else ''
            html = (
                '<!DOCTYPE html><html><head><title>Log in</title></head>'
                '<body style="font-family:sans-serif;display:flex;justify-content:center;padding-top:80px">'
                '<div style="width:360px">'
                '<h2>Red Education - Sign In</h2>'
                f'{error_html}'
                '<form method="post">'
                f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
                f'<input type="hidden" name="next" value="{request.GET.get("next", "/")}">'
                '<p><input name="username" placeholder="Username" style="width:100%;padding:8px" autofocus></p>'
                '<p><input name="password" type="password" placeholder="Password" style="width:100%;padding:8px"></p>'
                '<p><button type="submit" style="padding:8px 24px">Sign In</button></p>'
                '</form></div></body></html>'
            )
        return HttpResponse(html)


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
            try:
                html = render_to_string('404.html', request=request)
            except Exception:
                html = '<h1>404 — Page Not Found</h1>'
            return HttpResponseNotFound(html)

        logger.exception("Internal Server Error: %s", request.path)
        try:
            html = render_to_string('500.html')
        except Exception:
            html = '<h1>500 — Internal Server Error</h1>'
        return HttpResponseServerError(html)
