from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="Your phone number must start with 09 and be entered with English digits.",
)
