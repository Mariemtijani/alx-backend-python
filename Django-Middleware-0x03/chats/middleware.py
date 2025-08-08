# chats/middleware.py
from datetime import datetime
from django.contrib.auth.models import AnonymousUser
import os

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
