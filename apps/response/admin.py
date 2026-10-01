from django import forms
from django.contrib import admin
from django.utils.html import format_html

from apps.utility.models import Location, LocationType, PostalCode
from .models import Comment, Followup, Meeting, Response, VoiceRecording

class LocationChildMixin:

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)

        # Default
        form.base_fields["locality"].queryset = Location.objects.none()
        form.base_fields["area"].queryset = Location.objects.none()

        if obj and obj.city_id:
            form.base_fields["locality"].queryset = (
                Location.objects.filter(
                    parent_id=obj.city_id,
                    location_type=LocationType.LOCALITY_AREA,
                    is_active=True,
                ).order_by("name")
            )

        if obj and obj.locality_id:
            form.base_fields["area"].queryset = (
                Location.objects.filter(
                    parent_id=obj.locality_id,
                    location_type=LocationType.SUBLOCALITY_AREA,
                    is_active=True,
                ).order_by("name")
            )

        return form


class ResponseAdminForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["city"].queryset = Location.objects.filter(
            location_type=LocationType.DISTRICT_CITY,
            is_active=True,
        ).order_by("name")

        self.fields["locality"].queryset = Location.objects.none()
        self.fields["area"].queryset = Location.objects.none()
        self.fields["postal_code"].queryset = PostalCode.objects.none()

        city_id = self.data.get("city") or self.initial.get("city")
        locality_id = self.data.get("locality") or self.initial.get("locality")
        area_id = self.data.get("area") or self.initial.get("area")

        if not city_id and self.instance.pk:
            city_id = self.instance.city_id

        if not locality_id and self.instance.pk:
            locality_id = self.instance.locality_id

        if not area_id and self.instance.pk:
            area_id = self.instance.area_id

        if city_id:
            self.fields["locality"].queryset = (
                Location.objects.filter(
                    parent_id=city_id,
                    location_type=LocationType.LOCALITY_AREA,
                    is_active=True,
                ).order_by("name")
            )

        if locality_id:
            self.fields["area"].queryset = (
                Location.objects.filter(
                    parent_id=locality_id,
                    location_type=LocationType.SUBLOCALITY_AREA,
                    is_active=True,
                ).order_by("name")
            )

        if area_id:
            self.fields["postal_code"].queryset = (
                PostalCode.objects.filter(
                    location_id=area_id,
                    is_active=True,
                ).order_by("code")
            )


class AutoUserAdminMixin:

    def save_model(self, request, obj, form, change):
        if (
            hasattr(obj, "created_by")
            and not change
            and not getattr(obj, "created_by", None)
        ):
            obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        # Delete inline objects
        for obj in formset.deleted_objects:
            response = getattr(obj, "response", None)
            obj.delete()
            if response:
                response.refresh_status()

        # Save inline objects
        for obj in instances:
            if hasattr(obj, "created_by") and not getattr(
                obj, "created_by", None
            ):
                obj.created_by = request.user

            if hasattr(obj, "updated_by"):
                obj.updated_by = request.user

            obj.save()

            if hasattr(obj, "response"):
                obj.response.refresh_status()

        formset.save_m2m()


# =====================================================
# 🔹 MAGIC SEARCH MIXIN
# =====================================================


class MagicSearchMixin:
    prefix_map = {}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if not search_term:
            return queryset, use_distinct

        term = search_term.upper().strip()

        for prefix, field in self.prefix_map.items():
            if term.startswith(prefix):
                queryset |= self.model.objects.filter(**{field: term})

        if term.isdigit():
            if hasattr(self.model, "response"):
                queryset |= self.model.objects.filter(
                    response__contact_no__icontains=term
                )
            elif hasattr(self.model, "contact_no"):
                queryset |= self.model.objects.filter(
                    contact_no__icontains=term
                )

        return queryset, use_distinct


# =====================================================
# 🔹 INLINE CLASSES
# =====================================================


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True
    readonly_fields = (
        "meeting_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1
    max_num = 1
    can_delete = True
    show_change_link = True
    readonly_fields = (
        "followup_no",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    show_change_link = True
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    show_change_link = True
    readonly_fields = (
        "created_at",
        "created_by",
    )


# =====================================================
# 🔹 RESPONSE ADMIN & FORM
# =====================================================


@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, MagicSearchMixin, admin.ModelAdmin):

    save_on_top = True
    save_as = True
    save_as_continue = True

    list_per_page = 50

    prefix_map = {
        "R": "response_no",
    }

    STATUS_COLORS = {
        "New": "#2563eb",
        "Meeting": "#0ea5e9",
        "Follow_Up": "#f59e0b",
        "Meeting_FollowUp": "#8b5cf6",
        "Deal_close": "#16a34a",
        "Fake_lead": "#dc2626",
        "Training": "#7c3aed",
        "For_job": "#6366f1",
        "Software_company": "#0891b2",
        "Not_received": "#6b7280",
    }

    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
    ]

    list_display = (
        "response_id",
        "colored_status",
        "lead_source",
        "contact_no",
        "contact_persone",
        "business_name",
        "city",
        "assigned_to",
        "converted_badge",
        "created_at",
    )

    list_display_links = (
        "response_id",
        "contact_persone",
        "business_name",
    )

    search_fields = (
        "response_no",
        "contact_no",
        "contact_persone",
        "business_name",
    )

    list_filter = (
        "status",
        "lead_source",
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "is_converted",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_select_related = (
        "assigned_to",
        "business_category",
        "city",
        "locality",
        "area",
        "postal_code",
    )

    filter_horizontal = (
        "requirement_types",
    )

    readonly_fields = (
        "response_no",
        "converted_at",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    fieldsets = (

        (
            "Business Details",
            {
                "fields": (

                    "contact_no",
                    "contact_persone",
                    "business_name",
                    "status",

                    "business_category",
                    "lead_source",
                    "assigned_to",
                )
            },
        ),

        (
            "Location Details",
            {
                "fields": (
                    "city",
                    "locality",
                    "area",
                    "postal_code",
                    "address",
                )
            },
        ),

        (
            "Response Information",
            {
                "fields": (
                    "requirement_types",
                    "response_no",
                    "is_converted",
                    "converted_at",
                )
            },
        ),

        (
            "WhatsApp Tracking",
            {
                "classes": ("collapse",),
                "fields": (
                    "whatsapp_welcome_sent",
                    "whatsapp_followup_1_sent",
                    "whatsapp_followup_2_sent",
                ),
            },
        ),

        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    # ==========================================
    # Display Methods
    # ==========================================

    @admin.display(description="Response ID", ordering="response_no")
    def response_id(self, obj):
        return format_html(
            '<span style="font-weight:700;color:#2563eb;">{}</span>',
            obj.response_no,
        )

    @admin.display(description="Status", ordering="status")
    def colored_status(self, obj):

        color = self.STATUS_COLORS.get(
            obj.status,
            "#6b7280",
        )

        return format_html(
            '<span style="color:{};font-weight:700;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Conversion")
    def converted_badge(self, obj):

        color = "#16a34a" if obj.is_converted else "#dc2626"
        text = "Converted" if obj.is_converted else "Pending"

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:20px;font-weight:600;">{}</span>',
            color,
            text,
        )

    # ==========================================
    # ForeignKey Querysets
    # ==========================================

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "city":

            kwargs["queryset"] = (
                Location.objects.filter(
                    location_type=LocationType.DISTRICT_CITY,
                    is_active=True,
                ).order_by("name")
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )
# =====================================================
# 🔹 OTHER MODEL ADMINS
# =====================================================


@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    save_on_top = True

    list_per_page = 50

    ordering = (
        "-meeting_date",
    )

    list_select_related = (
        "response",
        "response__city",
        "response__locality",
        "assigned_to",
    )

    list_display = (
        "meeting_id",
        "response_id",
        "contact_person",
        "contact_no",
        "business_name",
        "lead_source",
        "city",
        "locality",
        "response_status",
        "meeting_status",
        "meeting_date",
        "assigned_to",
        "created_at",
    )

    list_display_links = (
        "meeting_id",
        "contact_person",
        "business_name",
    )

    search_fields = (
        "meeting_no",
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
    )

    list_filter = (
        "status",
        "meeting_date",
        "assigned_to",
        "response__city",
        "response__locality",
        "response__lead_source",
        "response__status",
    )

    @admin.display(description="Meeting ID", ordering="meeting_no")
    def meeting_id(self, obj):
        return obj.meeting_no

    @admin.display(description="Response ID", ordering="response__response_no")
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(description="Contact Person")
    def contact_person(self, obj):
        return obj.response.contact_persone

    @admin.display(description="Mobile")
    def contact_no(self, obj):
        return obj.response.contact_no

    @admin.display(description="Business")
    def business_name(self, obj):
        return obj.response.business_name

    @admin.display(description="Lead Source")
    def lead_source(self, obj):
        return obj.response.get_lead_source_display()

    @admin.display(description="City")
    def city(self, obj):
        return obj.response.city

    @admin.display(description="Locality")
    def locality(self, obj):
        return obj.response.locality

    @admin.display(description="Response Status")
    def response_status(self, obj):
        return obj.response.get_status_display()

    @admin.display(description="Meeting Status")
    def meeting_status(self, obj):
        return obj.get_status_display()



@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    save_on_top = True

    list_per_page = 50

    ordering = (
        "-followup_date",
    )

    list_select_related = (
        "response",
        "response__city",
        "response__locality",
        "assigned_to",
    )

    list_display = (
        "followup_id",
        "response_id",
        "contact_person",
        "contact_no",
        "business_name",
        "lead_source",
        "city",
        "locality",
        "response_status",
        "followup_status",
        "followup_date",
        "assigned_to",
        "created_at",
    )

    list_display_links = (
        "followup_id",
        "contact_person",
        "business_name",
    )

    search_fields = (
        "followup_no",
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
    )

    list_filter = (
        "status",
        "followup_date",
        "assigned_to",
        "response__city",
        "response__locality",
        "response__lead_source",
        "response__status",
    )

    @admin.display(description="Follow Up ID", ordering="followup_no")
    def followup_id(self, obj):
        return obj.followup_no

    @admin.display(description="Response ID", ordering="response__response_no")
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(description="Contact Person")
    def contact_person(self, obj):
        return obj.response.contact_persone

    @admin.display(description="Mobile")
    def contact_no(self, obj):
        return obj.response.contact_no

    @admin.display(description="Business")
    def business_name(self, obj):
        return obj.response.business_name

    @admin.display(description="Lead Source")
    def lead_source(self, obj):
        return obj.response.get_lead_source_display()

    @admin.display(description="City")
    def city(self, obj):
        return obj.response.city

    @admin.display(description="Locality")
    def locality(self, obj):
        return obj.response.locality

    @admin.display(description="Response Status")
    def response_status(self, obj):
        return obj.response.get_status_display()

    @admin.display(description="Follow Up Status")
    def followup_status(self, obj):
        return obj.get_status_display()


@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    save_on_top = True

    list_per_page = 50

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "response",
        "response__city",
        "response__locality",
        "created_by",
    )

    list_display = (
        "id",
        "response_id",
        "contact_person",
        "contact_no",
        "business_name",
        "lead_source",
        "city",
        "locality",
        "response_status",
        "short_comment",
        "created_by",
        "created_at",
    )

    list_display_links = (
        "id",
        "contact_person",
        "business_name",
    )

    search_fields = (
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
        "comment",
    )

    list_filter = (
        "created_at",
        "created_by",
        "response__city",
        "response__locality",
        "response__lead_source",
        "response__status",
    )

    @admin.display(description="Response ID", ordering="response__response_no")
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(description="Contact Person")
    def contact_person(self, obj):
        return obj.response.contact_persone

    @admin.display(description="Mobile")
    def contact_no(self, obj):
        return obj.response.contact_no

    @admin.display(description="Business")
    def business_name(self, obj):
        return obj.response.business_name

    @admin.display(description="Lead Source")
    def lead_source(self, obj):
        return obj.response.get_lead_source_display()

    @admin.display(description="City")
    def city(self, obj):
        return obj.response.city

    @admin.display(description="Locality")
    def locality(self, obj):
        return obj.response.locality

    @admin.display(description="Response Status")
    def response_status(self, obj):
        return obj.response.get_status_display()

    @admin.display(description="Comment")
    def short_comment(self, obj):
        if not obj.comment:
            return "-"
        return (
            obj.comment[:80] + "..."
            if len(obj.comment) > 80
            else obj.comment
        )
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):

    save_on_top = True

    list_per_page = 50

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "response",
        "response__city",
        "response__locality",
        "created_by",
    )

    list_display = (
        "id",
        "response_id",
        "contact_person",
        "contact_no",
        "business_name",
        "lead_source",
        "city",
        "locality",
        "response_status",
        "note",
        "audio_file",
        "created_by",
        "created_at",
    )

    list_display_links = (
        "id",
        "contact_person",
        "business_name",
    )

    search_fields = (
        "response__response_no",
        "response__contact_no",
        "response__contact_persone",
        "response__business_name",
        "note",
    )

    list_filter = (
        "created_at",
        "created_by",
        "response__city",
        "response__locality",
        "response__lead_source",
        "response__status",
    )

    @admin.display(description="Response ID", ordering="response__response_no")
    def response_id(self, obj):
        return obj.response.response_no

    @admin.display(description="Contact Person")
    def contact_person(self, obj):
        return obj.response.contact_persone

    @admin.display(description="Mobile")
    def contact_no(self, obj):
        return obj.response.contact_no

    @admin.display(description="Business")
    def business_name(self, obj):
        return obj.response.business_name

    @admin.display(description="Lead Source")
    def lead_source(self, obj):
        return obj.response.get_lead_source_display()

    @admin.display(description="City")
    def city(self, obj):
        return obj.response.city

    @admin.display(description="Locality")
    def locality(self, obj):
        return obj.response.locality

    @admin.display(description="Response Status")
    def response_status(self, obj):
        return obj.response.get_status_display()

    @admin.display(description="Audio")
    def audio_file(self, obj):
        if obj.file:
            return format_html(
                '<audio controls preload="none" style="width:180px;">'
                '<source src="{}">'
                "</audio>",
                obj.file.url,
            )
        return "-"