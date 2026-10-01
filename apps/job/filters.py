import django_filters
from django.db.models import Q

from .models import (
    Job,
    JobApplicant,
    InterviewSchedule,
    OfferLetter,
    EmployeeJoining,
)

from apps.companies.models import Company
from apps.utility.models import Location
from apps.job_utility.models import (
    JobCategory,
    JobIndustry,
)


# ==========================================================
# JOB FILTER
# ==========================================================

class JobFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(method="filter_keyword")

    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all()
    )

    category = django_filters.ModelChoiceFilter(
        queryset=JobCategory.objects.all()
    )

    industry = django_filters.ModelChoiceFilter(
        queryset=JobIndustry.objects.all()
    )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all()
    )

    featured = django_filters.BooleanFilter()

    published = django_filters.BooleanFilter()

    status = django_filters.CharFilter()

    job_type = django_filters.CharFilter()

    work_mode = django_filters.CharFilter()

    minimum_salary = django_filters.NumberFilter(
        field_name="minimum_salary",
        lookup_expr="gte",
    )

    maximum_salary = django_filters.NumberFilter(
        field_name="maximum_salary",
        lookup_expr="lte",
    )

    class Meta:

        model = Job

        fields = (
            "company",
            "category",
            "industry",
            "location",
            "featured",
            "published",
            "status",
            "job_type",
            "work_mode",
        )

    def filter_keyword(self, queryset, name, value):

        return queryset.filter(
            Q(title__name__icontains=value)
            | Q(company__name__icontains=value)
            | Q(short_description__icontains=value)
            | Q(description__icontains=value)
        ).distinct()


class JobApplicantFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(method="filter_keyword")

    experience_from = django_filters.NumberFilter(
        field_name="experience",
        lookup_expr="gte",
    )

    experience_to = django_filters.NumberFilter(
        field_name="experience",
        lookup_expr="lte",
    )

    expected_salary_from = django_filters.NumberFilter(
        field_name="expected_salary",
        lookup_expr="gte",
    )

    expected_salary_to = django_filters.NumberFilter(
        field_name="expected_salary",
        lookup_expr="lte",
    )

    class Meta:

        model = JobApplicant

        fields = (
            "job",
            "status",
            "source",
            "location",
        )

    def filter_keyword(self, queryset, name, value):

        return queryset.filter(
            Q(full_name__icontains=value)
            | Q(phone__icontains=value)
            | Q(email__icontains=value)
            | Q(current_company__icontains=value)
        ).distinct()


# ==========================================================
# INTERVIEW FILTER
# ==========================================================

class InterviewScheduleFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(method="filter_keyword")

    scheduled_from = django_filters.DateFilter(
        field_name="scheduled_datetime",
        lookup_expr="date__gte",
    )

    scheduled_to = django_filters.DateFilter(
        field_name="scheduled_datetime",
        lookup_expr="date__lte",
    )

    class Meta:

        model = InterviewSchedule

        fields = (
            "job",
            "interview_type",
            "status",
        )

    def filter_keyword(self, queryset, name, value):

        return queryset.filter(
            Q(applicant__full_name__icontains=value)
            | Q(interviewer__icontains=value)
            | Q(job__title__name__icontains=value)
        ).distinct()


# ==========================================================
# OFFER LETTER FILTER
# ==========================================================


class OfferLetterFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(method="filter_keyword")

    offer_date_from = django_filters.DateFilter(
        field_name="offer_date",
        lookup_expr="gte",
    )

    offer_date_to = django_filters.DateFilter(
        field_name="offer_date",
        lookup_expr="lte",
    )

    joining_from = django_filters.DateFilter(
        field_name="joining_date",
        lookup_expr="gte",
    )

    joining_to = django_filters.DateFilter(
        field_name="joining_date",
        lookup_expr="lte",
    )

    annual_ctc_from = django_filters.NumberFilter(
        field_name="annual_ctc",
        lookup_expr="gte",
    )

    annual_ctc_to = django_filters.NumberFilter(
        field_name="annual_ctc",
        lookup_expr="lte",
    )

    class Meta:

        model = OfferLetter

        fields = (
            "job",
            "status",
            "work_location",
        )

    def filter_keyword(self, queryset, name, value):

        return queryset.filter(
            Q(offer_number__icontains=value)
            | Q(applicant__full_name__icontains=value)
            | Q(designation__icontains=value)
            | Q(department__icontains=value)
        ).distinct()


# ==========================================================
# EMPLOYEE JOINING FILTER
# ==========================================================


class EmployeeJoiningFilter(django_filters.FilterSet):

    keyword = django_filters.CharFilter(method="filter_keyword")

    joining_from = django_filters.DateFilter(
        field_name="joining_date",
        lookup_expr="gte",
    )

    joining_to = django_filters.DateFilter(
        field_name="joining_date",
        lookup_expr="lte",
    )

    class Meta:

        model = EmployeeJoining

        fields = (
            "status",
            "department",
            "designation",
            "documents_verified",
            "id_card_issued",
            "welcome_mail_sent",
            "onboarding_completed",
        )

    def filter_keyword(self, queryset, name, value):

        return queryset.filter(
            Q(employee_code__icontains=value)
            | Q(applicant__full_name__icontains=value)
            | Q(designation__icontains=value)
            | Q(department__icontains=value)
            | Q(manager__icontains=value)
        ).distinct()


# ==========================================================
# COMMON FILTER MIXIN
# ==========================================================


class ActiveJobFilter(django_filters.BooleanFilter):

    def filter(self, qs, value):

        if value:
            return qs.filter(
                published=True,
                status="ACTIVE",
            )

        return qs


class FeaturedJobFilter(django_filters.BooleanFilter):

    def filter(self, qs, value):

        if value:
            return qs.filter(featured=True)

        return qs



