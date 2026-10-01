from django import forms
from django.contrib import admin
from django.utils.html import format_html
from apps.utility.resources import LocationResource
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.utility.models import (
    Location,
    PostalCode,
    LocationType,
)

from ..filters import (
    StateFilter,
    DistrictCityFilter,
    LocalityFilter,
)


# ==========================================================
# Location Admin Form
# ==========================================================

class LocationAdminForm(forms.ModelForm):
    

    class Meta:
        model = Location
        fields = "__all__"

    class Media:
        js = (
            "admin/js/jquery.init.js",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        parent_map = {
            LocationType.STATE: [LocationType.COUNTRY],
            LocationType.DISTRICT_CITY: [LocationType.STATE],
            LocationType.LOCALITY_AREA: [LocationType.DISTRICT_CITY],
            LocationType.SUBLOCALITY_AREA: [LocationType.LOCALITY_AREA],
        }

        location_type = None

        # POST request
        if self.data.get("location_type"):
            location_type = self.data.get("location_type")

        # Edit page
        elif self.instance.pk:
            location_type = self.instance.location_type

        # Parent queryset
        if location_type in parent_map:

            self.fields["parent"].queryset = (
                Location.objects.filter(
                    location_type__in=parent_map[location_type],
                    is_active=True,
                )
                .order_by("name")
            )

        elif location_type == LocationType.COUNTRY:

            self.fields["parent"].queryset = (
                Location.objects.none()
            )

        else:

            self.fields["parent"].queryset = (
                Location.objects.filter(
                    is_active=True
                ).order_by(
                    "tree_id",
                    "lft"
                )
            )

        self.fields["parent"].required = False




# ==========================================================
# Location Admin
# ==========================================================

@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):

    resource_class = LocationResource   # ✅ Yahin hona chahiye

    form = LocationAdminForm


    mptt_indent_field = "name"

    autocomplete_fields = (
        "parent",
    )

    list_display = (
        "tree_actions",
        "indented_title",
        "parent",
        "location_badge",
        "is_top_city",
        "is_active",
    )

    list_display_links = (
        "indented_title",
    )

    list_editable = (
        "is_top_city",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "slug",
        "parent__name",
    )

    list_filter = (
        "location_type",
        StateFilter,
        DistrictCityFilter,
        LocalityFilter,
        "is_top_city",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "tree_id",
        "lft",
    )

    save_on_top = True

    list_per_page = 50

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "name",
                "code",
                "slug",
                "description",
            )
        }),

        ("Hierarchy", {
            "fields": (
                "location_type",
                "parent",
                "display_order",
            )
        }),

        ("Status", {
            "fields": (
                "is_top_city",
                "is_active",
            )
        }),

        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Type")
    def location_badge(self, obj):

        colors = {
            LocationType.COUNTRY: "#0d6efd",
            LocationType.STATE: "#198754",
            LocationType.DISTRICT_CITY: "#fd7e14",
            LocationType.LOCALITY_AREA: "#20c997",
            LocationType.SUBLOCALITY_AREA: "#dc3545",
        }

        color = colors.get(
            obj.location_type,
            "#6c757d",
        )

        return format_html(
            """
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:20px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            """,
            color,
            obj.get_location_type_display(),
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("parent")
        )



# ==========================================================
# Admin Actions
# ==========================================================

    actions = (
        "make_active",
        "make_inactive",
        "make_top_city",
        "remove_top_city",
    )

    @admin.action(description="✅ Mark selected locations as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Mark selected locations as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="⭐ Mark selected locations as Top City")
    def make_top_city(self, request, queryset):
        queryset.update(is_top_city=True)

    @admin.action(description="Remove Top City")
    def remove_top_city(self, request, queryset):
        queryset.update(is_top_city=False)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# ==========================================================
# Postal Code Admin
# ==========================================================

@admin.register(PostalCode)
class PostalCodeAdmin(ImportExportModelAdmin):

    list_display = (
        "code",
        "location",
        "location_type",
        "is_active",
    )

    list_display_links = (
        "code",
    )

    search_fields = (
        "code",
        "location__name",
    )

    autocomplete_fields = (
        "location",
    )

    list_filter = (
        "location__location_type",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "code",
    )

    save_on_top = True

    list_per_page = 50

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("location")
        )

    @admin.display(description="Location Type")
    def location_type(self, obj):
        if obj.location:
            return obj.location.get_location_type_display()
        return "-"


# ==========================================================
# Admin Actions
# ==========================================================

    actions = (
        "make_active",
        "make_inactive",
        "make_top_city",
        "remove_top_city",
    )

    @admin.action(description="✅ Mark selected locations as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Mark selected locations as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="⭐ Mark selected locations as Top City")
    def make_top_city(self, request, queryset):
        queryset.update(is_top_city=True)

    @admin.action(description="Remove Top City")
    def remove_top_city(self, request, queryset):
        queryset.update(is_top_city=False)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# ==========================================================
# Postal Code Admin
# ==========================================================
