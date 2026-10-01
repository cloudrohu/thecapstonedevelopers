from django.core.exceptions import ValidationError


def validate_indian_mobile(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError(
            "Enter a valid 10 digit mobile number."
        )