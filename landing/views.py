from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LeadForm
from .services import send_lead_to_telegram

LEAD_COOKIE_NAME = "lead_submitted"
LEAD_COOKIE_MAX_AGE = 60 * 60 * 24  # 1 day


def home(request):
    form_submitted = request.COOKIES.get(LEAD_COOKIE_NAME) == "1"
    form = LeadForm(request.POST or None)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method == "POST":
        if form.is_valid():
            success, error_message = send_lead_to_telegram(
                form.cleaned_data["name"],
                form.cleaned_data["phone"],
                form.cleaned_data.get("message", ""),
            )
            if success:
                if is_ajax:
                    response = JsonResponse(
                        {"status": "ok", "message": "Заявка отправлена. Мы скоро свяжемся!"}
                    )
                else:
                    response = HttpResponseRedirect(reverse("home"))
                response.set_cookie(
                    LEAD_COOKIE_NAME,
                    "1",
                    max_age=LEAD_COOKIE_MAX_AGE,
                    samesite="Lax",
                    secure=not settings.DEBUG,
                )
                return response
            message = error_message or "Не удалось отправить заявку. Попробуйте позже."
            if is_ajax:
                return JsonResponse(
                    {"status": "error", "message": message},
                    status=500,
                )
            form.add_error(None, message)
        else:
            if is_ajax:
                return JsonResponse(
                    {"status": "error", "errors": form.errors},
                    status=400,
                )
            # fall-through renders template with errors

    context = {
        "form": form,
        "form_submitted": form_submitted,
    }
    return render(request, "home.html", context)


def privacy(request):
    return render(request, "privacy.html")
