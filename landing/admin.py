"""
Кастомная админка для редактирования контента лендинга через удобные формы.
"""
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.contrib import messages

from .content import load_content, save_content


class HeroForm(forms.Form):
    """Форма для редактирования Hero-секции."""
    title = forms.CharField(
        label="Заголовок",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    lead = forms.CharField(
        label="Подзаголовок",
        widget=forms.Textarea(attrs={"rows": 4, "class": "vLargeTextField", "style": "width: 100%;"}),
        help_text="Каждая строка будет на новой строке на сайте",
    )
    cta_text = forms.CharField(
        label="Текст кнопки",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )


class ContactsForm(forms.Form):
    """Форма для редактирования контактов."""
    phone = forms.CharField(
        label="Телефон",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )
    schedule = forms.CharField(
        label="График работы",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    telegram_link = forms.URLField(
        label="Ссылка на Telegram",
        widget=forms.URLInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    telegram_label = forms.CharField(
        label="Текст ссылки Telegram",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )


class HowWeWorkForm(forms.Form):
    """Форма для редактирования секции 'Как мы работаем'."""
    title = forms.CharField(
        label="Заголовок секции",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    subtitle = forms.CharField(
        label="Подзаголовок секции",
        max_length=300,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    # Шаги (до 7)
    step1_title = forms.CharField(label="Шаг 1 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step1_text = forms.CharField(label="Шаг 1 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step2_title = forms.CharField(label="Шаг 2 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step2_text = forms.CharField(label="Шаг 2 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step3_title = forms.CharField(label="Шаг 3 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step3_text = forms.CharField(label="Шаг 3 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step4_title = forms.CharField(label="Шаг 4 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step4_text = forms.CharField(label="Шаг 4 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step5_title = forms.CharField(label="Шаг 5 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step5_text = forms.CharField(label="Шаг 5 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step6_title = forms.CharField(label="Шаг 6 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step6_text = forms.CharField(label="Шаг 6 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))
    step7_title = forms.CharField(label="Шаг 7 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    step7_text = forms.CharField(label="Шаг 7 — описание", max_length=500, required=False, widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}))


class WhyChooseUsForm(forms.Form):
    """Форма для редактирования секции 'Почему выбирают нас'."""
    title = forms.CharField(
        label="Заголовок секции",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    card1_title = forms.CharField(label="Карточка 1 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card1_text = forms.CharField(label="Карточка 1 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    card2_title = forms.CharField(label="Карточка 2 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card2_text = forms.CharField(label="Карточка 2 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    card3_title = forms.CharField(label="Карточка 3 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card3_text = forms.CharField(label="Карточка 3 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))


class WhySellForm(forms.Form):
    """Форма для редактирования секции 'Зачем продавать остатки'."""
    title = forms.CharField(
        label="Заголовок секции",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    subtitle = forms.CharField(
        label="Подзаголовок секции",
        max_length=300,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    card1_title = forms.CharField(label="Карточка 1 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card1_text = forms.CharField(label="Карточка 1 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    card2_title = forms.CharField(label="Карточка 2 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card2_text = forms.CharField(label="Карточка 2 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    card3_title = forms.CharField(label="Карточка 3 — заголовок", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    card3_text = forms.CharField(label="Карточка 3 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))


class ReviewsForm(forms.Form):
    """Форма для редактирования отзывов."""
    title = forms.CharField(
        label="Заголовок секции",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    # До 6 отзывов
    review1_quote = forms.CharField(label="Отзыв 1 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review1_author = forms.CharField(label="Отзыв 1 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review1_role = forms.CharField(label="Отзыв 1 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review2_quote = forms.CharField(label="Отзыв 2 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review2_author = forms.CharField(label="Отзыв 2 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review2_role = forms.CharField(label="Отзыв 2 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review3_quote = forms.CharField(label="Отзыв 3 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review3_author = forms.CharField(label="Отзыв 3 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review3_role = forms.CharField(label="Отзыв 3 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review4_quote = forms.CharField(label="Отзыв 4 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review4_author = forms.CharField(label="Отзыв 4 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review4_role = forms.CharField(label="Отзыв 4 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review5_quote = forms.CharField(label="Отзыв 5 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review5_author = forms.CharField(label="Отзыв 5 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review5_role = forms.CharField(label="Отзыв 5 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review6_quote = forms.CharField(label="Отзыв 6 — текст", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2, "class": "vLargeTextField", "style": "width: 100%;"}))
    review6_author = forms.CharField(label="Отзыв 6 — автор", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))
    review6_role = forms.CharField(label="Отзыв 6 — должность", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "vTextField"}))


class ContactFormForm(forms.Form):
    """Форма для редактирования секции контактной формы."""
    title = forms.CharField(
        label="Заголовок секции",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    subtitle = forms.CharField(
        label="Подзаголовок секции",
        max_length=300,
        widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"}),
    )
    success_message = forms.CharField(
        label="Сообщение после отправки",
        widget=forms.Textarea(attrs={"rows": 3, "class": "vLargeTextField", "style": "width: 100%;"}),
        help_text="Каждая строка будет на новой строке",
    )
    submit_button = forms.CharField(
        label="Текст кнопки отправки",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )


def _get_list_item(lst, index, default=None):
    """Безопасно получить элемент списка по индексу."""
    try:
        return lst[index] if lst and len(lst) > index else default
    except (TypeError, IndexError):
        return default


def _content_to_forms(content):
    """Преобразует JSON-контент в initial-данные для форм."""
    hero = content.get("hero", {})
    contacts = content.get("contacts", {})
    how_we_work = content.get("how_we_work", {})
    why_choose_us = content.get("why_choose_us", {})
    why_sell = content.get("why_sell", {})
    reviews = content.get("reviews", {})
    contact_form = content.get("contact_form", {})

    # Hero
    hero_initial = {
        "title": hero.get("title", ""),
        "lead": hero.get("lead", ""),
        "cta_text": hero.get("cta_text", ""),
    }

    # Contacts
    contacts_initial = {
        "phone": contacts.get("phone", ""),
        "schedule": contacts.get("schedule", ""),
        "telegram_link": contacts.get("telegram_link", ""),
        "telegram_label": contacts.get("telegram_label", ""),
    }

    # How we work
    steps = how_we_work.get("steps", [])
    how_we_work_initial = {
        "title": how_we_work.get("title", ""),
        "subtitle": how_we_work.get("subtitle", ""),
    }
    for i in range(1, 8):
        step = _get_list_item(steps, i - 1, {})
        how_we_work_initial[f"step{i}_title"] = step.get("title", "") if step else ""
        how_we_work_initial[f"step{i}_text"] = step.get("text", "") if step else ""

    # Why choose us
    cards = why_choose_us.get("cards", [])
    why_choose_us_initial = {"title": why_choose_us.get("title", "")}
    for i in range(1, 4):
        card = _get_list_item(cards, i - 1, {})
        why_choose_us_initial[f"card{i}_title"] = card.get("title", "") if card else ""
        why_choose_us_initial[f"card{i}_text"] = card.get("text", "") if card else ""

    # Why sell
    cards = why_sell.get("cards", [])
    why_sell_initial = {
        "title": why_sell.get("title", ""),
        "subtitle": why_sell.get("subtitle", ""),
    }
    for i in range(1, 4):
        card = _get_list_item(cards, i - 1, {})
        why_sell_initial[f"card{i}_title"] = card.get("title", "") if card else ""
        why_sell_initial[f"card{i}_text"] = card.get("text", "") if card else ""

    # Reviews
    items = reviews.get("items", [])
    reviews_initial = {"title": reviews.get("title", "")}
    for i in range(1, 7):
        item = _get_list_item(items, i - 1, {})
        reviews_initial[f"review{i}_quote"] = item.get("quote", "") if item else ""
        reviews_initial[f"review{i}_author"] = item.get("author", "") if item else ""
        reviews_initial[f"review{i}_role"] = item.get("role", "") if item else ""

    # Contact form
    contact_form_initial = {
        "title": contact_form.get("title", ""),
        "subtitle": contact_form.get("subtitle", ""),
        "success_message": contact_form.get("success_message", ""),
        "submit_button": contact_form.get("submit_button", ""),
    }

    return {
        "hero": hero_initial,
        "contacts": contacts_initial,
        "how_we_work": how_we_work_initial,
        "why_choose_us": why_choose_us_initial,
        "why_sell": why_sell_initial,
        "reviews": reviews_initial,
        "contact_form": contact_form_initial,
    }


def _forms_to_content(hero_data, contacts_data, how_we_work_data, why_choose_us_data, why_sell_data, reviews_data, contact_form_data):
    """Преобразует данные форм обратно в JSON-структуру."""
    # Steps
    steps = []
    for i in range(1, 8):
        title = how_we_work_data.get(f"step{i}_title", "").strip()
        text = how_we_work_data.get(f"step{i}_text", "").strip()
        if title or text:
            steps.append({"title": title, "text": text})

    # Why choose us cards
    why_choose_us_cards = []
    for i in range(1, 4):
        title = why_choose_us_data.get(f"card{i}_title", "").strip()
        text = why_choose_us_data.get(f"card{i}_text", "").strip()
        if title or text:
            why_choose_us_cards.append({"title": title, "text": text})

    # Why sell cards
    why_sell_cards = []
    for i in range(1, 4):
        title = why_sell_data.get(f"card{i}_title", "").strip()
        text = why_sell_data.get(f"card{i}_text", "").strip()
        if title or text:
            why_sell_cards.append({"title": title, "text": text})

    # Reviews
    review_items = []
    for i in range(1, 7):
        quote = reviews_data.get(f"review{i}_quote", "").strip()
        author = reviews_data.get(f"review{i}_author", "").strip()
        role = reviews_data.get(f"review{i}_role", "").strip()
        if quote or author:
            review_items.append({"quote": quote, "author": author, "role": role})

    return {
        "hero": {
            "title": hero_data.get("title", ""),
            "lead": hero_data.get("lead", ""),
            "cta_text": hero_data.get("cta_text", ""),
        },
        "contacts": {
            "phone": contacts_data.get("phone", ""),
            "schedule": contacts_data.get("schedule", ""),
            "telegram_link": contacts_data.get("telegram_link", ""),
            "telegram_label": contacts_data.get("telegram_label", ""),
        },
        "how_we_work": {
            "title": how_we_work_data.get("title", ""),
            "subtitle": how_we_work_data.get("subtitle", ""),
            "steps": steps,
        },
        "why_choose_us": {
            "title": why_choose_us_data.get("title", ""),
            "cards": why_choose_us_cards,
        },
        "why_sell": {
            "title": why_sell_data.get("title", ""),
            "subtitle": why_sell_data.get("subtitle", ""),
            "cards": why_sell_cards,
        },
        "reviews": {
            "title": reviews_data.get("title", ""),
            "items": review_items,
        },
        "contact_form": {
            "title": contact_form_data.get("title", ""),
            "subtitle": contact_form_data.get("subtitle", ""),
            "success_message": contact_form_data.get("success_message", ""),
            "submit_button": contact_form_data.get("submit_button", ""),
        },
    }


class ContentAdminSite(admin.AdminSite):
    """Расширенная админка с возможностью редактирования контента."""
    site_header = "Панель управления сайтом"
    site_title = "Админ-панель"
    index_title = "Управление контентом"
    
    enable_nav_sidebar = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("content/", self.admin_view(self.content_edit_view), name="content_edit"),
        ]
        return custom_urls + urls

    def content_edit_view(self, request):
        """Вью для редактирования контента через удобные формы."""
        content = load_content()
        initials = _content_to_forms(content)

        if request.method == "POST":
            hero_form = HeroForm(request.POST, prefix="hero")
            contacts_form = ContactsForm(request.POST, prefix="contacts")
            how_we_work_form = HowWeWorkForm(request.POST, prefix="how_we_work")
            why_choose_us_form = WhyChooseUsForm(request.POST, prefix="why_choose_us")
            why_sell_form = WhySellForm(request.POST, prefix="why_sell")
            reviews_form = ReviewsForm(request.POST, prefix="reviews")
            contact_form_form = ContactFormForm(request.POST, prefix="contact_form")

            all_valid = all([
                hero_form.is_valid(),
                contacts_form.is_valid(),
                how_we_work_form.is_valid(),
                why_choose_us_form.is_valid(),
                why_sell_form.is_valid(),
                reviews_form.is_valid(),
                contact_form_form.is_valid(),
            ])

            if all_valid:
                new_content = _forms_to_content(
                    hero_form.cleaned_data,
                    contacts_form.cleaned_data,
                    how_we_work_form.cleaned_data,
                    why_choose_us_form.cleaned_data,
                    why_sell_form.cleaned_data,
                    reviews_form.cleaned_data,
                    contact_form_form.cleaned_data,
                )
                if save_content(new_content):
                    messages.success(request, "Контент успешно сохранён!")
                    return HttpResponseRedirect(request.path)
                else:
                    messages.error(request, "Ошибка сохранения контента.")
        else:
            hero_form = HeroForm(initial=initials["hero"], prefix="hero")
            contacts_form = ContactsForm(initial=initials["contacts"], prefix="contacts")
            how_we_work_form = HowWeWorkForm(initial=initials["how_we_work"], prefix="how_we_work")
            why_choose_us_form = WhyChooseUsForm(initial=initials["why_choose_us"], prefix="why_choose_us")
            why_sell_form = WhySellForm(initial=initials["why_sell"], prefix="why_sell")
            reviews_form = ReviewsForm(initial=initials["reviews"], prefix="reviews")
            contact_form_form = ContactFormForm(initial=initials["contact_form"], prefix="contact_form")

        context = {
            **self.each_context(request),
            "hero_form": hero_form,
            "contacts_form": contacts_form,
            "how_we_work_form": how_we_work_form,
            "why_choose_us_form": why_choose_us_form,
            "why_sell_form": why_sell_form,
            "reviews_form": reviews_form,
            "contact_form_form": contact_form_form,
            "title": "Редактирование контента сайта",
            "opts": {"app_label": "landing"},
        }
        return render(request, "admin/content_edit.html", context)

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["content_edit_url"] = "admin:content_edit"
        return super().index(request, extra_context)


admin_site = ContentAdminSite(name="admin")

# Регистрируем встроенные модели Django
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
