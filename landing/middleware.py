import hashlib
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse


ADMIN_LOGIN_THROTTLE_SECONDS = 60
ADMIN_LOGIN_MAX_ATTEMPTS = 5


class AdminLoginThrottleMiddleware:
    """Throttling для формы входа в админку."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/admin/login/" and request.method == "POST":
            ip = self._get_client_ip(request)
            cache_key = f"admin_login_attempts:{ip}"
            attempts = cache.get(cache_key, 0)

            if attempts >= ADMIN_LOGIN_MAX_ATTEMPTS:
                return HttpResponse(
                    "Слишком много попыток входа. Попробуйте через минуту.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )

            response = self.get_response(request)

            if response.status_code == 200 and "login" in request.path:
                cache.set(cache_key, attempts + 1, ADMIN_LOGIN_THROTTLE_SECONDS)

            return response

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")


class LeadThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and self._should_throttle(request.path):
            client_id = self._client_key(request)
            last_hit = cache.get(client_id)
            throttle_seconds = settings.LEAD_THROTTLE_SECONDS

            if last_hit and time.time() - last_hit < throttle_seconds:
                retry_after = int(throttle_seconds - (time.time() - last_hit))
                response_data = {
                    "status": "error",
                    "message": "Слишком много запросов. Попробуйте еще раз позже.",
                    "retry_after": retry_after,
                }
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse(response_data, status=429)
                resp = HttpResponse(response_data["message"], status=429)
                resp["Retry-After"] = str(retry_after)
                return resp

            cache.set(client_id, time.time(), throttle_seconds)

        response = self.get_response(request)
        return response

    def _should_throttle(self, path: str) -> bool:
        return any(
            path.startswith(p.rstrip("/")) if p != "/" else path == p or path == ""
            for p in settings.THROTTLED_PATHS
        )

    def _client_key(self, request) -> str:
        user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
        ip = request.META.get("REMOTE_ADDR", "ip")
        fingerprint = f"{ip}:{user_agent}".encode("utf-8", "ignore")
        hashed = hashlib.sha256(fingerprint).hexdigest()
        return f"lead_throttle:{hashed}"
