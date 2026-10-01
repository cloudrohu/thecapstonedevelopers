from django.utils.text import slugify


def generate_slug(text):
    return slugify(text)