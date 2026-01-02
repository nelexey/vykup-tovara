from django.conf import settings


def _clean_phone_for_tel(phone: str) -> str:
    allowed = {"+", "-", " "}
    return "".join(ch for ch in phone if ch.isdigit() or ch in allowed).replace(" ", "")


def site_contacts(request):
    phone = settings.CONTACT_PHONE
    return {
        "contact_phone": phone,
        "contact_phone_tel": _clean_phone_for_tel(phone),
        "contact_schedule": settings.CONTACT_SCHEDULE,
        "telegram_link": settings.TELEGRAM_LINK,
        "telegram_label": settings.TELEGRAM_LABEL,
    }
