from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin
from .resources import (
    DeveloperResource,
    MeetingResource,
    FollowupResource,
)

from .models import *

from .models import (
    Developer,
    Architects,
    Engineer,
    Project,

    BookingOffer,
    WelcomeTo,
    WebSlider,
    Overview,
    AboutUs,
    USP,
    Configuration,
    Connectivity,
    Amenities,
    Gallery,
    Header,
    RERA_Info,
    WhyInvest,
    BankOffer,
    ProjectFAQ,
    Enquiry,
    ProjectContactPerson,

    Comment,
    VoiceRecording,
    Visit,
    Followup,
    Meeting,
    DeveloperImpactMetric
)

NO_IMAGE = "https://via.placeholder.com/70x70?text=No+Image"


class BaseAdmin(admin.ModelAdmin):

    save_on_top = True

    list_per_page = 30

    actions = (
        "make_active",
        "make_inactive",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.action(description="✅ Mark selected as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Mark selected as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def save_model(self, request, obj, form, change):

        if hasattr(obj, "created_by"):

            if not obj.pk:
                obj.created_by = request.user

        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )



class ImagePreviewMixin:

    image_field = "image"

    def image_preview(self, obj):

        image = getattr(obj, self.image_field, None)

        if image and hasattr(image, "url"):
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                image.url,
            )

        return "-"

    image_preview.short_description = "Preview"


class LogoPreviewMixin:

    logo_field = "logo"

    def logo_preview(self, obj):

        logo = getattr(obj, self.logo_field, None)

        if logo and hasattr(logo, "url"):

            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                logo.url,
            )

        return "-"

    logo_preview.short_description = "Logo"


class BaseCRMInline(admin.TabularInline):
    extra = 1

    def get_exclude(self, request, obj=None):
        exclude = [
            "developer",
            "architect",
            "engineer",
            "project",
            "type",
        ]

        # Parent FK ko exclude mat karo
        if hasattr(self, "fk_name") and self.fk_name in exclude:
            exclude.remove(self.fk_name)

        return tuple(exclude)


class BaseCRMAdmin(ImportExportModelAdmin):

    save_on_top = True

    list_per_page = 50

    def save_model(self, request, obj, form, change):

        if not change and not obj.created_by:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    search_fields = (
        "title",
        "contact_person",
        "contact_no",
        "email",
    )

    list_filter = (
        "is_active",
        "is_verified",
        "is_featured",
        "calling_status",
    )

    list_editable = (
        "is_active",
        "is_verified",
        "is_featured",
    )

    ordering = (
        "-created_at",
    )

    def logo_preview(self, obj):
        logo = getattr(obj, "logo", None)

        if logo and hasattr(logo, "url"):
            return format_html(
                '<img src="{}" style="height:55px;border-radius:6px;">',
                logo.url,
            )

        return "-"

    logo_preview.short_description = "Logo"

class CommentDeveloperInline(BaseCRMInline):
    model = Comment
    fk_name = "developer"
    extra = 1


class CommentArchitectInline(BaseCRMInline):
    model = Comment
    fk_name = "architect"
    extra = 1


class CommentEngineerInline(BaseCRMInline):
    model = Comment
    fk_name = "engineer"
    extra = 1


class CommentProjectInline(BaseCRMInline):
    model = Comment
    fk_name = "project"
    extra = 1



class VoiceDeveloperInline(BaseCRMInline):
    model = VoiceRecording
    fk_name = "developer"
    extra = 1


class VoiceArchitectInline(BaseCRMInline):
    model = VoiceRecording
    fk_name = "architect"
    extra = 1


class VoiceEngineerInline(BaseCRMInline):
    model = VoiceRecording
    fk_name = "engineer"
    extra = 1


class VoiceProjectInline(BaseCRMInline):
    model = VoiceRecording
    fk_name = "project"
    extra = 1



class VisitDeveloperInline(BaseCRMInline):
    model = Visit
    fk_name = "developer"
    extra = 1


class VisitArchitectInline(BaseCRMInline):
    model = Visit
    fk_name = "architect"
    extra = 1


class VisitEngineerInline(BaseCRMInline):
    model = Visit
    fk_name = "engineer"
    extra = 1


class VisitProjectInline(BaseCRMInline):
    model = Visit
    fk_name = "project"
    extra = 1



class FollowupDeveloperInline(BaseCRMInline):
    model = Followup
    fk_name = "developer"
    extra = 1


class FollowupArchitectInline(BaseCRMInline):
    model = Followup
    fk_name = "architect"
    extra = 1


class FollowupEngineerInline(BaseCRMInline):
    model = Followup
    fk_name = "engineer"
    extra = 1


class FollowupProjectInline(BaseCRMInline):
    model = Followup
    fk_name = "project"
    extra = 1



class MeetingDeveloperInline(BaseCRMInline):
    model = Meeting
    fk_name = "developer"
    extra = 1


    exclude = (
        "architect",
        "engineer",
        "project",
        'type'
    )



class MeetingArchitectInline(BaseCRMInline):
    model = Meeting
    fk_name = "architect"
    extra = 1


class MeetingEngineerInline(BaseCRMInline):
    model = Meeting
    fk_name = "engineer"
    extra = 1


class MeetingProjectInline(BaseCRMInline):
    model = Meeting
    fk_name = "project"
    extra = 1




# =====================================================
# PROJECT INLINES
# =====================================================

class BookingOfferInline(BaseCRMInline):
    model = BookingOffer
    extra = 1


class WelcomeToInline(admin.StackedInline):
    model = WelcomeTo
    extra = 1


class WebSliderInline(BaseCRMInline):
    model = WebSlider
    extra = 1


class OverviewInline(BaseCRMInline):
    model = Overview
    extra = 1


class AboutUsInline(admin.StackedInline):
    model = AboutUs
    extra = 1


class USPInline(BaseCRMInline):
    model = USP
    extra = 1


class ConfigurationInline(BaseCRMInline):
    model = Configuration
    extra = 1


class ConnectivityInline(BaseCRMInline):
    model = Connectivity
    extra = 1


class AmenitiesInline(BaseCRMInline):
    model = Amenities
    extra = 1


class GalleryInline(BaseCRMInline):
    model = Gallery
    extra = 1


class HeaderInline(admin.StackedInline):
    model = Header
    extra = 1
    max_num = 1


class RERAInline(admin.StackedInline):
    model = RERA_Info
    extra = 1
    max_num = 1


class WhyInvestInline(BaseCRMInline):
    model = WhyInvest
    extra = 1


class BankOfferInline(BaseCRMInline):
    model = BankOffer
    extra = 1


class FAQInline(BaseCRMInline):
    model = ProjectFAQ
    extra = 1

class DeveloperImpactMetricInline(admin.TabularInline):
    model = DeveloperImpactMetric
    fk_name = "setting"

    min_num = 0
    can_delete = True

    fields = (
        "title",
        "value",
        "icon",
        "order",
    )

    ordering = ("order",)
    show_change_link = False



class ContactPersonInline(BaseCRMInline):
    model = ProjectContactPerson
    extra = 1


class EnquiryInline(BaseCRMInline):
    model = Enquiry
    extra = 1
    can_delete = False
    readonly_fields = (
        "name",
        "phone",
        "email",
        "message",
        "contacted_on",
    )

@admin.register(Developer)
class DeveloperAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ):
    change_list_template = "admin/properties/developer/change_list.html"
    

    resource_class = DeveloperResource

    list_display = ("id",
        "title",
        "city",
        "locality",
        "contact_person",
        "contact_no",
        "calling_status",
        "featured_builder",
        "is_active",
        "logo_preview",
        
    )



    list_editable = (
        "featured_builder",
        "is_active",
    )

    search_fields = (
        "title",
        "slug",
        "contact_person",
        "contact_no",
        "email",
        "city__name",
        "locality__name",
        "postal_code__code",
    )

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )

    list_filter = (
        "calling_status",
        "featured_builder",
        "is_verified",
        "is_active",
        "city",
    )
    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        CommentDeveloperInline,
        VoiceDeveloperInline,
        VisitDeveloperInline,
        FollowupDeveloperInline,
        DeveloperImpactMetricInline,
        MeetingDeveloperInline,
    ]

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "logo",
                "logo_preview",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_person",
                "contact_no",
                "email",
                "web_site",
            )
        }),

        ("Description", {
            "fields": (
                "keywords",
                "about_developer",
                "read_more",
                "note",
            )
        }),

        ("Status", {
            "fields": (
                "calling_status",
                "assigned_to",
                "featured_builder",
                "is_featured",
                "is_verified",
                "is_active",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    save_on_top = True
    list_per_page = 15


    # =====================================================
    # CHANGE VIEW
    # =====================================================

    def change_view(
        self,
        request,
        object_id,
        form_url="",
        extra_context=None,
    ):
        """
        Remember where Developer was opened from.

        Possible sources:
            Meeting
            Followup
        """

        if request.method == "GET":

            return_to = request.GET.get("return_to")

            meeting_id = request.GET.get("meeting_id")

            followup_id = request.GET.get("followup_id")


            # =================================================
            # OPENED FROM MEETING
            # =================================================

            if return_to == "meeting" and meeting_id:

                request.session[
                    f"developer_return_{object_id}"
                ] = {
                    "return_to": "meeting",
                    "meeting_id": meeting_id,
                }


            # =================================================
            # OPENED FROM FOLLOWUP
            # =================================================

            elif return_to == "followup" and followup_id:

                request.session[
                    f"developer_return_{object_id}"
                ] = {
                    "return_to": "followup",
                    "followup_id": followup_id,
                }


        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


    # =====================================================
    # AFTER SAVE
    # =====================================================

    def response_change(
        self,
        request,
        obj,
    ):
        """
        After saving Developer:

        Meeting  -> same Meeting card
        Followup -> same Followup card
        Direct   -> normal Developer list
        """

        from django.http import HttpResponseRedirect


        # =================================================
        # GET SAVED RETURN DATA
        # =================================================

        return_data = request.session.pop(
            f"developer_return_{obj.pk}",
            None,
        )


        # =================================================
        # RETURN TO MEETING
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "meeting"
                and return_data.get("meeting_id")
            ):

                meeting_id = return_data["meeting_id"]


                return HttpResponseRedirect(
                    f"/admin/properties/meeting/"
                    f"#meeting-{meeting_id}"
                )


        # =================================================
        # RETURN TO FOLLOWUP
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "followup"
                and return_data.get("followup_id")
            ):

                followup_id = return_data["followup_id"]


                return HttpResponseRedirect(
                    f"/admin/properties/followup/"
                    f"#followup-{followup_id}"
                )


        # =================================================
        # NORMAL DJANGO ADMIN SAVE
        # =================================================

        return super().response_change(
            request,
            obj,
        )


@admin.register(Architects)
class ArchitectAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ):

    inlines = [
        CommentArchitectInline,
        VoiceArchitectInline,
        VisitArchitectInline,
        FollowupArchitectInline,
        MeetingArchitectInline,
    ]
    
    list_display = (
            "title",
            "city",
            "locality",
            "contact_person",
            "contact_no",
            "calling_status",
            "featured_architect",
            "is_active",
            "logo_preview",
        )

    list_display_links = ("title",)

    list_editable = (
        "featured_architect",
        "is_active",
    )

    search_fields = (
        "title",
        "slug",
        "contact_person",
        "contact_no",
        "email",
        "city__name",
        "locality__name",
        "postal_code__code",
    )

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )

    list_filter = (
        "calling_status",
        "featured_architect",
        "is_verified",
        "is_active",
        "city",
    )

    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "logo",
                "logo_preview",
            )
        }),

        ("Location", {
            "fields": (
                "city",
                "locality",
                "area",
                "postal_code",
                "address",
                "google_map",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_person",
                "contact_no",
                "email",
                "web_site",
            )
        }),

        ("Description", {
            "fields": (
                "keywords",
                "about_architect",
                "note",
            )
        }),

        ("Status", {
            "fields": (
                "calling_status",
                "assigned_to",
                "featured_architect",
                "is_featured",
                "is_verified",
                "is_active",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


    save_on_top = True
    list_per_page = 30


    # =====================================================
    # CHANGE VIEW
    # =====================================================

    def change_view(
        self,
        request,
        object_id,
        form_url="",
        extra_context=None,
    ):
        """
        Remember where Architect was opened from.

        Possible sources:
            Meeting
            Followup
        """

        if request.method == "GET":

            return_to = request.GET.get("return_to")

            meeting_id = request.GET.get("meeting_id")

            followup_id = request.GET.get("followup_id")


            # =================================================
            # OPENED FROM MEETING
            # =================================================

            if return_to == "meeting" and meeting_id:

                request.session[
                    f"architect_return_{object_id}"
                ] = {
                    "return_to": "meeting",
                    "meeting_id": meeting_id,
                }


            # =================================================
            # OPENED FROM FOLLOWUP
            # =================================================

            elif return_to == "followup" and followup_id:

                request.session[
                    f"architect_return_{object_id}"
                ] = {
                    "return_to": "followup",
                    "followup_id": followup_id,
                }


        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


    # =====================================================
    # AFTER SAVE
    # =====================================================

    def response_change(
        self,
        request,
        obj,
    ):
        """
        After saving Architect:

        Meeting  -> same Meeting card
        Followup -> same Followup card
        Direct   -> normal Architect list
        """

        from django.http import HttpResponseRedirect


        # =================================================
        # GET SAVED RETURN DATA
        # =================================================

        return_data = request.session.pop(
            f"architect_return_{obj.pk}",
            None,
        )


        # =================================================
        # RETURN TO MEETING
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "meeting"
                and return_data.get("meeting_id")
            ):

                meeting_id = return_data["meeting_id"]


                return HttpResponseRedirect(
                    f"/admin/properties/meeting/"
                    f"#meeting-{meeting_id}"
                )


        # =================================================
        # RETURN TO FOLLOWUP
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "followup"
                and return_data.get("followup_id")
            ):

                followup_id = return_data["followup_id"]


                return HttpResponseRedirect(
                    f"/admin/properties/followup/"
                    f"#followup-{followup_id}"
                )


        # =================================================
        # NORMAL DJANGO ADMIN SAVE
        # =================================================

        return super().response_change(
            request,
            obj,
        )

#ImportExportModelAdmin

@admin.register(Engineer)
class EngineerAdmin(
    BaseAdmin,
    LogoPreviewMixin,
    ):

    # =================================================
    # SEARCH
    # =================================================

    search_fields = (
        "title",
        "slug",
        "contact_person",
        "contact_no",
        "email",
        "city__name",
        "locality__name",
        "postal_code__code",
    )


    # =================================================
    # AUTOCOMPLETE
    # =================================================

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
        "assigned_to",
    )


    # =================================================
    # FILTER
    # =================================================

    list_filter = (
        "calling_status",
        "featured_engineer",
        "is_verified",
        "is_active",
        "city",
    )


    # =================================================
    # READONLY
    # =================================================

    readonly_fields = (
        "slug",
        "logo_preview",
        "created_at",
        "updated_at",
    )


    # =================================================
    # LIST DISPLAY
    # =================================================

    list_display = (
        "title",
        "city",
        "locality",
        "contact_person",
        "contact_no",
        "calling_status",
        "featured_engineer",
        "is_active",
        "logo_preview",
    )


    list_display_links = (
        "title",
    )


    list_editable = (
        "featured_engineer",
        "is_active",
    )


    # =================================================
    # INLINE
    # =================================================

    inlines = [
        CommentEngineerInline,
        VoiceEngineerInline,
        VisitEngineerInline,
        FollowupEngineerInline,
        MeetingEngineerInline,
    ]


    # =================================================
    # CHANGE VIEW
    # =================================================

    def change_view(
        self,
        request,
        object_id,
        form_url="",
        extra_context=None,
    ):

        if request.method == "GET":

            return_to = request.GET.get("return_to")

            meeting_id = request.GET.get("meeting_id")

            followup_id = request.GET.get("followup_id")


            # -----------------------------
            # FROM MEETING
            # -----------------------------

            if return_to == "meeting" and meeting_id:

                request.session[
                    f"engineer_return_{object_id}"
                ] = {
                    "return_to": "meeting",
                    "meeting_id": meeting_id,
                }


            # -----------------------------
            # FROM FOLLOWUP
            # -----------------------------

            elif return_to == "followup" and followup_id:

                request.session[
                    f"engineer_return_{object_id}"
                ] = {
                    "return_to": "followup",
                    "followup_id": followup_id,
                }


        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


    # =================================================
    # AFTER SAVE
    # =================================================

    def response_change(
        self,
        request,
        obj,
    ):

        from django.http import HttpResponseRedirect


        return_data = request.session.pop(
            f"engineer_return_{obj.pk}",
            None,
        )


        # =================================================
        # RETURN TO MEETING
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "meeting"
                and return_data.get("meeting_id")
            ):

                meeting_id = return_data["meeting_id"]

                return HttpResponseRedirect(
                    f"/admin/properties/meeting/"
                    f"#meeting-{meeting_id}"
                )


        # =================================================
        # RETURN TO FOLLOWUP
        # =================================================

        if return_data:

            if (
                return_data.get("return_to") == "followup"
                and return_data.get("followup_id")
            ):

                followup_id = return_data["followup_id"]

                return HttpResponseRedirect(
                    f"/admin/properties/followup/"
                    f"#followup-{followup_id}"
                )


        # =================================================
        # NORMAL DJANGO SAVE
        # =================================================

        return super().response_change(
            request,
            obj,
        )


@admin.register(Project)
class ProjectAdmin(BaseAdmin,ImagePreviewMixin,ImportExportModelAdmin,DraggableMPTTAdmin,):
    image_field = "image"
    mptt_indent_field = "project_name"

    list_display = ('id',
        "tree_actions",
        "indented_title",
        "developer",
        "city",
        "locality",
        "construction_status",
        "featured_property",
        "is_active",
        "image_preview",
    )



    list_editable = (
        "featured_property",
        "is_active",
    )

    search_fields = (
        "project_name",
        "developer__title",
        "city__name",
        "locality__name",
        "slug",
    )

    autocomplete_fields = (
        "parent",
        "developer",
        "architect",
        "engineer",
        "city",
        "locality",
        "area",
        "postal_code",
        "property_type",
        "possession_year",
    )

    list_filter = (
        "construction_status",
        "featured_property",
        "is_active",
        "developer",
        "city",
        "property_type",
    )

    readonly_fields = (
        "slug",
        "image_preview",
        "created_at",
        "updated_at",
    )

    

    ordering = (
        "tree_id",
        "lft",
    )

    save_on_top = True

    list_per_page = 20

    inlines = [
        HeaderInline,
        WelcomeToInline,
        WebSliderInline,
        OverviewInline,
        AboutUsInline,
        GalleryInline,


        ConfigurationInline,
        ConnectivityInline,
        AmenitiesInline,
        WhyInvestInline,
        BankOfferInline,
        FAQInline,
        USPInline,

        BookingOfferInline,
        RERAInline,

        ContactPersonInline,
        EnquiryInline,
                # CRM

        CommentProjectInline,
        VoiceProjectInline,
        VisitProjectInline,
        FollowupProjectInline,
        MeetingProjectInline,
    ]

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "parent",
                "project_name",
                "property_type",

                "city",
                "locality",
                "developer",

                "architect",
                "engineer",
                "construction_status",

                "bhk_type",
                "possession_year",
                "possession_month",
                "occupancy_certificate",
                "commencement_certificate",
                "calling_status",
                "image",
                "youtube_embed_id",
                "featured_property",
                "is_active",
                "slug",
                "image_preview",
            )
        }),



        ("Location", {
            "fields": (
                
                "area",
                "postal_code",
                "address",
                "google_map_iframe",
            )
        }),

        ("Configuration", {
            "fields": (
                "floor",
                "land_parcel",
                "luxurious",
                "pricing",
                "balcony",
            )
        }),


        
    )


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"
    # =====================================================
# RETURN TO MEETING AFTER EDITING PROJECT
# =====================================================

    def change_view(
        self,
        request,
        object_id,
        form_url="",
        extra_context=None,
    ):
        """
        Remember if Project was opened from a Meeting.
        """

        if request.method == "GET":

            return_to = request.GET.get("return_to")
            meeting_id = request.GET.get("meeting_id")

            if return_to == "meeting" and meeting_id:

                request.session[
                    f"project_return_{object_id}"
                ] = {
                    "return_to": "meeting",
                    "meeting_id": meeting_id,
                }

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


    def response_change(self, request, obj):
        """
        After saving Project, return to the same Meeting card.
        """

        return_data = request.session.pop(
            f"project_return_{obj.pk}",
            None,
        )

        if return_data:

            if (
                return_data.get("return_to") == "meeting"
                and return_data.get("meeting_id")
            ):

                from django.http import HttpResponseRedirect

                meeting_id = return_data["meeting_id"]

                return HttpResponseRedirect(
                    f"/admin/properties/meeting/#meeting-{meeting_id}"
                )

        return super().response_change(
            request,
            obj,
        )




# =====================================================
# VOICE RECORDING
# =====================================================

@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):

    list_display = (
        "type",
        "developer",
        "architect",
        "engineer",
        "project",
        "uploaded_by",
        "created_at",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "uploaded_by",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
    )

    list_filter = (
        "type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30


# =====================================================
# VISIT
# =====================================================

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    change_list_template = "admin/properties/visit/change_list.html"


    list_display = (
        "type",
        "visit_for",
        "visit_type",
        "visit_status",
        "developer",
        "architect",
        "engineer",
        "project",
        "created_at",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "created_by",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "visit_for",
        "visit_status",
        "visit_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

# ImportExportModelAdmin
@admin.register(Followup)
class FollowupAdmin(
    BaseAdmin,
    ImagePreviewMixin,
    ):

    resource_class = FollowupResource

    change_list_template = "admin/properties/followup/change_list.html"

    list_display = (
        "type",
        "status",
        "followup_date",
        "assigned_to",
        "developer",
        "architect",
        "engineer",
        "project",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "assigned_to",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-followup_date",
    )

    list_per_page = 30
# =====================================================
# MEETING ImportExportModelAdmin
# =====================================================

@admin.register(Meeting)
class MeetingAdmin(
    BaseAdmin,
    ImagePreviewMixin,
    ):

    resource_class = MeetingResource

    change_list_template = "admin/properties/meeting/change_list.html"

    # baaki tumhara existing code...

    list_display = (
        "type",
        "status",
        "meeting_date",
        "assigned_to",
        "developer",
        "architect",
        "engineer",
        "project",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "assigned_to",
    )

    search_fields = (
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
        "comment",
    )

    list_filter = (
        "type",
        "status",
        "meeting_date",
        "assigned_to",
    )

    readonly_fields = (
            "created_at",
            "updated_at",
        )

    ordering = (
        "-meeting_date",
    )

    list_per_page = 30
# =====================================================
# BASE ADMIN
# =====================================================




# =====================================================
# COMMENT ADMIN
# =====================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    change_list_template = "admin/properties/comment/change_list.html"

    list_display = (
        "type",
        "parent_name",
        "comment_preview",
        "created_by",
        "created_at",
    )

    list_display_links = (
        "comment_preview",
    )

    autocomplete_fields = (
        "developer",
        "architect",
        "engineer",
        "project",
        "created_by",
        "updated_by",
    )

    search_fields = (
        "comment",
        "developer__title",
        "architect__title",
        "engineer__title",
        "project__project_name",
    )

    list_filter = (
        "type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    fieldsets = (
        ("Comment Information", {
            "fields": (
                "type",
                "comment",
            )
        }),

        ("Parent", {
            "fields": (
                "developer",
                "architect",
                "engineer",
                "project",
            )
        }),

        ("System", {
            "classes": ("collapse",),
            "fields": (
                "created_by",
                "created_at",
                "updated_by",
                "updated_at",
            )
        }),
    )

    def parent_name(self, obj):
        if obj.project:
            return obj.project.project_name

        if obj.developer:
            return obj.developer.title

        if obj.architect:
            return obj.architect.title

        if obj.engineer:
            return obj.engineer.title

        return "-"

    parent_name.short_description = "Parent"

    def comment_preview(self, obj):
        if not obj.comment:
            return "-"

        text = obj.comment.strip()

        if len(text) > 80:
            return f"{text[:80]}..."

        return text

    comment_preview.short_description = "Comment"

    def save_model(self, request, obj, form, change):

        if not change and not obj.created_by:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )