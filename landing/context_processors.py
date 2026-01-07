from django.conf import settings

from .content import load_content


def _clean_phone_for_tel(phone: str) -> str:
    allowed = {"+", "-", " "}
    return "".join(ch for ch in phone if ch.isdigit() or ch in allowed).replace(" ", "")


def site_contacts(request):
    content = load_content()
    contacts = content.get("contacts", {})
    phone = contacts.get("phone") or settings.CONTACT_PHONE
    return {
        "contact_phone": phone,
        "contact_phone_tel": _clean_phone_for_tel(phone),
        "contact_schedule": contacts.get("schedule") or settings.CONTACT_SCHEDULE,
        "telegram_link": contacts.get("telegram_link") or settings.TELEGRAM_LINK,
        "telegram_label": contacts.get("telegram_label") or settings.TELEGRAM_LABEL,
    }


def landing_content(request):
    """Передаёт весь редактируемый контент в шаблоны."""
    return {"content": load_content()}
