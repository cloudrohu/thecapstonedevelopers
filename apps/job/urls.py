from django.urls import path

from .views import (
    DashboardView,

    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,

    JobApplicantListView,
    JobApplicantDetailView,
    JobApplicantCreateView,
    JobApplicantUpdateView,
    JobApplicantDeleteView,

    ApplicantStatusUpdateView,
    ApplicantShortlistView,
    ApplicantRejectView,

    InterviewScheduleListView,
    InterviewScheduleCreateView,
    InterviewScheduleUpdateView,
    InterviewScheduleDeleteView,

    OfferLetterListView,
    OfferLetterCreateView,
    OfferLetterUpdateView,
    OfferLetterDeleteView,

    EmployeeJoiningListView,
    EmployeeJoiningCreateView,
    EmployeeJoiningUpdateView,
    EmployeeJoiningDeleteView,

    DashboardStatsView,
)

app_name = "job"

urlpatterns = [

    # ======================================================
    # Dashboard
    # ======================================================

    path(
        "",
        DashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "dashboard/stats/",
        DashboardStatsView.as_view(),
        name="dashboard_stats",
    ),

    # ======================================================
    # Jobs
    # ======================================================

    path(
        "jobs/",
        JobListView.as_view(),
        name="job_list",
    ),

    path(
        "jobs/create/",
        JobCreateView.as_view(),
        name="job_create",
    ),

    path(
        "jobs/<int:pk>/",
        JobDetailView.as_view(),
        name="job_detail",
    ),

    path(
        "jobs/<int:pk>/edit/",
        JobUpdateView.as_view(),
        name="job_update",
    ),

    path(
        "jobs/<int:pk>/delete/",
        JobDeleteView.as_view(),
        name="job_delete",
    ),

    # ======================================================
    # Applicants
    # ======================================================

    path(
        "applicants/",
        JobApplicantListView.as_view(),
        name="job_applicant_list",
    ),

    path(
        "applicants/create/",
        JobApplicantCreateView.as_view(),
        name="job_applicant_create",
    ),

    path(
        "applicants/<int:pk>/",
        JobApplicantDetailView.as_view(),
        name="job_applicant_detail",
    ),

    path(
        "applicants/<int:pk>/edit/",
        JobApplicantUpdateView.as_view(),
        name="job_applicant_update",
    ),

    path(
        "applicants/<int:pk>/delete/",
        JobApplicantDeleteView.as_view(),
        name="job_applicant_delete",
    ),

    path(
        "applicants/<int:pk>/status/",
        ApplicantStatusUpdateView.as_view(),
        name="applicant_status",
    ),

    path(
        "applicants/<int:pk>/shortlist/",
        ApplicantShortlistView.as_view(),
        name="applicant_shortlist",
    ),

    path(
        "applicants/<int:pk>/reject/",
        ApplicantRejectView.as_view(),
        name="applicant_reject",
    ),

    # ======================================================
    # Interviews
    # ======================================================

    path(
        "interviews/",
        InterviewScheduleListView.as_view(),
        name="interview_list",
    ),

    path(
        "interviews/create/",
        InterviewScheduleCreateView.as_view(),
        name="interview_create",
    ),

    path(
        "interviews/<int:pk>/edit/",
        InterviewScheduleUpdateView.as_view(),
        name="interview_update",
    ),

    path(
        "interviews/<int:pk>/delete/",
        InterviewScheduleDeleteView.as_view(),
        name="interview_delete",
    ),

    # ======================================================
    # Offers
    # ======================================================

    path(
        "offers/",
        OfferLetterListView.as_view(),
        name="offer_list",
    ),

    path(
        "offers/create/",
        OfferLetterCreateView.as_view(),
        name="offer_create",
    ),

    path(
        "offers/<int:pk>/edit/",
        OfferLetterUpdateView.as_view(),
        name="offer_update",
    ),

    path(
        "offers/<int:pk>/delete/",
        OfferLetterDeleteView.as_view(),
        name="offer_delete",
    ),

    # ======================================================
    # Employee Joining
    # ======================================================

    path(
        "joining/",
        EmployeeJoiningListView.as_view(),
        name="joining_list",
    ),

    path(
        "joining/create/",
        EmployeeJoiningCreateView.as_view(),
        name="joining_create",
    ),

    path(
        "joining/<int:pk>/edit/",
        EmployeeJoiningUpdateView.as_view(),
        name="joining_update",
    ),

    path(
        "joining/<int:pk>/delete/",
        EmployeeJoiningDeleteView.as_view(),
        name="joining_delete",
    ),

]