"""
Модуль для работы с редактируемым контентом лендинга.
Контент хранится в JSON-файле и загружается при каждом запросе.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

CONTENT_FILE = Path(settings.BASE_DIR) / "data" / "content.json"

DEFAULT_CONTENT: dict[str, Any] = {
    "hero": {
        "title": "Хватит терпеть убытки!",
        "lead": "Маркетплейсы «закрутили гайки», а вы всё ещё держитесь?\nПродайте остатки — сохраните часть прибыли!\nВаши остатки — наша забота. Выкупаем быстро, платим сразу и работаем со всеми площадками.",
        "cta_text": "Оставить заявку"
    },
    "contacts": {
        "phone": "+7 (929) 464-65-00",
        "schedule": "Ежедневно с 09 до 22 часов",
        "telegram_link": "https://t.me/vykuptovara",
        "telegram_label": "в Telegram"
    },
    "how_we_work": {
        "title": "Как мы работаем",
        "subtitle": "От заявки до получения денег — 5 простых шагов",
        "steps": []
    },
    "why_choose_us": {
        "title": "Почему выбирают нас",
        "cards": []
    },
    "why_sell": {
        "title": "Зачем продавать остатки",
        "subtitle": "Хранение неликвида обходится дороже, чем кажется",
        "cards": []
    },
    "reviews": {
        "title": "Отзывы клиентов",
        "items": []
    },
    "contact_form": {
        "title": "Оставьте заявку",
        "subtitle": "Расскажите о товаре — мы свяжемся и сделаем предложение",
        "success_message": "Спасибо! Ваша заявка принята.\nМы свяжемся с вами в ближайшее время.",
        "submit_button": "Отправить заявку"
    }
}


def load_content() -> dict[str, Any]:
    """Загружает контент из JSON-файла. При ошибке возвращает дефолтный контент."""
    if not CONTENT_FILE.exists():
        return DEFAULT_CONTENT.copy()
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Ошибка загрузки контента из %s: %s", CONTENT_FILE, e)
        return DEFAULT_CONTENT.copy()


def save_content(data: dict[str, Any]) -> bool:
    """Сохраняет контент в JSON-файл. Возвращает True при успехе."""
    try:
        CONTENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except OSError as e:
        logger.error("Ошибка сохранения контента в %s: %s", CONTENT_FILE, e)
        return False
