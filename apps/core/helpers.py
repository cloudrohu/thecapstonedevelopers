from django.contrib import messages


def success(request, text):
    messages.success(request, text)


def error(request, text):
    messages.error(request, text)