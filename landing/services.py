from __future__ import annotations

from typing import Tuple

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TELEGRAM_API_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"


def send_lead_to_telegram(name: str, phone: str, note: str = "") -> Tuple[bool, str | None]:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_ids = settings.TELEGRAM_CHAT_IDS or []

    if not token or not chat_ids:
        return False, "Telegram бот не настроен. Укажите TOKEN и CHAT_ID в .env"

    message_lines = [
        "Новая заявка с лендинга",
        f"Имя: {name}",
        f"Телефон: {phone}",
    ]
    if note.strip():
        message_lines.append(f"Комментарий: {note.strip()[:500]}")

    message = "\n".join(message_lines)
    url = TELEGRAM_API_TEMPLATE.format(token=token)

    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": True,
        }
        try:
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as error:
            logger.exception("Ошибка при отправке заявки в Telegram (chat_id=%s)", chat_id)
            return False, "Не удалось отправить заявку. Попробуйте позже."

    return True, None
