
NO_IMAGE_URL = "https://via.placeholder.com/80x80.png?text=No+Image"

from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import (
    Find_Form,
    Googlemap_Status,
    Call_Status,
    SocialSite,
    Meeting_Followup_Type,
    RequirementType,
    Response_Status,
    PropertyType,
    PossessionIn,
    ProjectAmenities,
    Bank,
    PropertyAmenities,
    UnitType,
    Furnishing,
    Facing,
    ConstructionStatus,
    OwnershipType,
    ParkingType,
    Amenity,
)


# ==========================================================
# SIMPLE MASTER ADMIN
# ==========================================================

class BaseMasterAdmin(ImportExportModelAdmin):
    list_per_page = 30
    ordering = ("id",)


@admin.register(Find_Form)
class FindFormAdmin(BaseMasterAdmin):
    list_display = ("id", "title", "create_at")
    search_fields = ("title",)


@admin.register(Googlemap_Status)
class GoogleMapStatusAdmin(BaseMasterAdmin):
    list_display = ("id", "title", "create_at")
    search_fields = ("title",)


@admin.register(Call_Status)
class CallStatusAdmin(BaseMasterAdmin):
    list_display = ("id", "title", "create_at")
    search_fields = ("title",)


@admin.register(SocialSite)
class SocialSiteAdmin(BaseMasterAdmin):
    list_display = ("id", "title", "code")
    search_fields = ("title", "code")


@admin.register(Meeting_Followup_Type)
class MeetingFollowupTypeAdmin(BaseMasterAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(RequirementType)
class RequirementTypeAdmin(BaseMasterAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Response_Status)
class ResponseStatusAdmin(BaseMasterAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(PossessionIn)
class PossessionInAdmin(BaseMasterAdmin):
    list_display = ("id", "year")
    search_fields = ("year",)
    ordering = ("year",)


# ==========================================================
# PROPERTY TYPE
# ==========================================================

@admin.register(PropertyType)
class PropertyTypeAdmin(DraggableMPTTAdmin):

    mptt_indent_field = "name"

    list_display = (
        "tree_actions",
        "indented_title",
        "parent",
        "is_top_level",
        "is_selectable",
    )

    list_filter = (
        "is_top_level",
        "is_selectable",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_per_page = 30


# ==========================================================
# PROJECT AMENITIES
# ==========================================================

@admin.register(ProjectAmenities)
class ProjectAmenitiesAdmin(BaseMasterAdmin):

    list_display = (
        "id",
        "title",
        "image_preview",
    )

    search_fields = ("title",)

    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" style="border-radius:6px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"


# ==========================================================
# PROPERTY AMENITIES
# ==========================================================

@admin.register(PropertyAmenities)
class PropertyAmenitiesAdmin(BaseMasterAdmin):

    list_display = (
        "id",
        "name",
        "icon_preview",
    )

    search_fields = ("name",)

    readonly_fields = ("icon_preview",)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" />',
                obj.icon.url,
            )
        return "-"

    icon_preview.short_description = "Icon"


# ==========================================================
# BANK
# ==========================================================

@admin.register(Bank)
class BankAdmin(BaseMasterAdmin):

    list_display = (
        "id",
        "title",
        "logo_preview",
    )

    search_fields = ("title",)

    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:6px;" />',
                obj.image.url,
            )
        return "-"

    logo_preview.short_description = "Logo"


# ==========================================================
# BASE NAME ADMIN
# ==========================================================

class BaseNameAdmin(BaseMasterAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(UnitType)
class UnitTypeAdmin(BaseNameAdmin):
    pass


@admin.register(Furnishing)
class FurnishingAdmin(BaseNameAdmin):
    pass


@admin.register(Facing)
class FacingAdmin(BaseNameAdmin):
    pass


@admin.register(ConstructionStatus)
class ConstructionStatusAdmin(BaseNameAdmin):
    pass


@admin.register(OwnershipType)
class OwnershipTypeAdmin(BaseNameAdmin):
    pass


@admin.register(ParkingType)
class ParkingTypeAdmin(BaseNameAdmin):
    pass


# ==========================================================
# AMENITY
# ==========================================================

@admin.register(Amenity)
class AmenityAdmin(BaseMasterAdmin):

    list_display = (
        "id",
        "name",
        "icon",
    )

    search_fields = (
        "name",
        "icon",
    )