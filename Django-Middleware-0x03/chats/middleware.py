# chats/middleware.py
from datetime import datetime
from django.contrib.auth.models import AnonymousUser
import os
from django.http import HttpResponseForbidden
from django.utils import timezone

class RequestLoggingMiddleware:
    """
    Logs each request as:
        f"{datetime.now()} - User: {user} - Path: {request.path}"
    into requests.log at the project root.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # log file beside manage.py (project root)
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requests.log")

    def __call__(self, request):
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else AnonymousUser()
        line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # append to log
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            # don’t break the request if logging fails
            pass

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    """
    Deny access outside 09:00–18:00 (server time).
    Returns 403 for any request made outside that window.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 9   # 09:00
        self.end_hour = 18    # 18:00

    def __call__(self, request):
        now = timezone.now()  # timezone-aware
        hour = now.hour

        # Block if current hour is before 09:00 or at/after 18:00
        if hour < self.start_hour or hour >= self.end_hour:
            return HttpResponseForbidden(
                "Access restricted to business hours (09:00–18:00)."
            )

        return self.get_response(request)