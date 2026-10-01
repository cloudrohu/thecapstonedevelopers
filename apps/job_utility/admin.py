from django.contrib import admin
from .models import (
    JobTitle,
    JobCategory,
    JobIndustry,
    JobSkill,
    JobBenefit,
    JobAsset,
    JobDocument,
    JobLanguageRequirement,
    SalaryType,
    WorkingDaysOption,
    JobTimingTemplate,
)
from import_export.admin import ImportExportModelAdmin

class BaseUtilityAdmin(ImportExportModelAdmin):
    list_per_page = 50
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobTitle)
class JobTitleAdmin(BaseUtilityAdmin):
    list_display = ("id", "name", "is_active")
    list_filter = ("is_active",)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "jobtitle", "is_active")
    list_filter = ("jobtitle", "is_active")
    search_fields = ("name", "jobtitle__name")
    autocomplete_fields = ("jobtitle",)
    ordering = ("name",)


@admin.register(JobIndustry)
class JobIndustryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ("name", "jobtitle")
    list_filter = ("jobtitle",)
    search_fields = ("name", "jobtitle__name")
    autocomplete_fields = ("jobtitle",)
    ordering = ("name",)


@admin.register(JobBenefit)
class JobBenefitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobAsset)
class JobAssetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobDocument)
class JobDocumentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobLanguageRequirement)
class JobLanguageRequirementAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(SalaryType)
class SalaryTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(WorkingDaysOption)
class WorkingDaysOptionAdmin(admin.ModelAdmin):
    list_display = ("label",)
    search_fields = ("label",)
    ordering = ("label",)


@admin.register(JobTimingTemplate)
class JobTimingTemplateAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time")
    ordering = ("start_time",)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("start_time")