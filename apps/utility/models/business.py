from django.db import models

from .base import MasterBaseModel


class LeadSource(MasterBaseModel):
    """
    Where the lead originated.
    """

    class Meta:
        verbose_name = "Lead Source"
        verbose_name_plural = "Lead Sources"
        ordering = ["name"]

    def __str__(self):
        return self.name



class LeadStatus(MasterBaseModel):
    """
    Status of a lead.
    """

    color = models.CharField(
        max_length=20,
        default="#6c757d",
        help_text="Hex color used in CRM badges.",
    )

    class Meta:
        verbose_name = "Lead Status"
        verbose_name_plural = "Lead Statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name


class LeadPriority(MasterBaseModel):
    class Meta:
        verbose_name = "Lead Priority"
        verbose_name_plural = "Lead Priorities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class InquiryType(MasterBaseModel):
    class Meta:
        verbose_name = "Inquiry Type"
        verbose_name_plural = "Inquiry Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RequirementType(MasterBaseModel):
    class Meta:
        verbose_name = "Requirement Type"
        verbose_name_plural = "Requirement Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContactType(MasterBaseModel):
    class Meta:
        verbose_name = "Contact Type"
        verbose_name_plural = "Contact Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Occupation(MasterBaseModel):
    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"
        ordering = ["name"]

    def __str__(self):
        return self.name



class CompanyType(MasterBaseModel):
    class Meta:
        verbose_name = "Company Type"
        verbose_name_plural = "Company Types"
        ordering = ["name"]

    def __str__(self):
        return self.name