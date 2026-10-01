from django.contrib import admin

from apps.utility.models import (
    LeadSource,
    LeadStatus,
    LeadPriority,
    InquiryType,
    RequirementType,
    ContactType,
    Occupation,
    CompanyType,
)

from .base import MasterAdmin, ColorMasterAdmin


@admin.register(LeadSource)
class LeadSourceAdmin(MasterAdmin):
    pass


@admin.register(LeadPriority)
class LeadPriorityAdmin(MasterAdmin):
    pass


@admin.register(InquiryType)
class InquiryTypeAdmin(MasterAdmin):
    pass


@admin.register(RequirementType)
class RequirementTypeAdmin(MasterAdmin):
    pass


@admin.register(ContactType)
class ContactTypeAdmin(MasterAdmin):
    pass


@admin.register(Occupation)
class OccupationAdmin(MasterAdmin):
    pass


@admin.register(CompanyType)
class CompanyTypeAdmin(MasterAdmin):
    pass


@admin.register(LeadStatus)
class LeadStatusAdmin(ColorMasterAdmin):
    list_display = (
        "name",
        "code",
        "color_preview",
        "is_active",
    )