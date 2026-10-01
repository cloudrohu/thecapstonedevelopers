from .base import MasterBaseModel

from django.db import models
class Language(MasterBaseModel):
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Currency(MasterBaseModel):
    symbol = models.CharField(
        max_length=10,
        blank=True,
    )

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CountryCode(MasterBaseModel):
    dial_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Country Code"
        verbose_name_plural = "Country Codes"

    def __str__(self):
        return f"{self.name} ({self.dial_code})"


class Religion(MasterBaseModel):
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Education(MasterBaseModel):
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MaritalStatus(MasterBaseModel):
    class Meta:
        verbose_name = "Marital Status"
        verbose_name_plural = "Marital Statuses"

    def __str__(self):
        return self.name