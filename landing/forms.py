from django import forms
from django.core.validators import RegexValidator


class LeadForm(forms.Form):
    phone_validator = RegexValidator(
        regex=r"^\+7\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$",
        message="Введите номер в формате +7 (XXX) XXX-XX-XX",
    )

    name = forms.CharField(
        label="",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше имя",
                "class": "form-input",
                "autocomplete": "off",
                "required": "required",
            }
        ),
        error_messages={"required": "Введите ваше имя"},
    )
    phone = forms.CharField(
        label="",
        max_length=50,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7 (___) ___-__-__",
                "class": "form-input",
                "autocomplete": "tel",
                "required": "required",
                "id": "phone-input",
                "inputmode": "tel",
            }
        ),
        error_messages={"required": "Укажите номер телефона"},
    )
    message = forms.CharField(
        label="",
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Опишите задачу или товар (до 500 символов, необязательно)",
                "class": "form-textarea",
                "rows": 4,
            }
        ),
    )
    consent = forms.BooleanField(
        label="",
        error_messages={"required": "Необходимо согласие на обработку данных"},
    )
