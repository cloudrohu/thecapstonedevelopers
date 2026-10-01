from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import (
    Job,
    JobApplicant,
    InterviewSchedule,
    OfferLetter,
    EmployeeJoining,
)

from .forms import (
    JobForm,
    JobApplicantForm,
    InterviewScheduleForm,
    OfferLetterForm,
    EmployeeJoiningForm,
)


from .filters import (
    JobFilter,
    JobApplicantFilter,
)


# ==========================================================
# DASHBOARD
# ==========================================================

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "jobs/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_jobs"] = Job.objects.count()

        context["active_jobs"] = Job.objects.filter(
            status="ACTIVE",
            published=True,
        ).count()

        context["featured_jobs"] = Job.objects.filter(
            featured=True,
        ).count()

        context["total_applicants"] = JobApplicant.objects.count()

        context["selected_applicants"] = JobApplicant.objects.filter(
            status="SELECTED",
        ).count()

        context["joined_employees"] = EmployeeJoining.objects.filter(
            status="JOINED",
        ).count()

        context["upcoming_interviews"] = (
            InterviewSchedule.objects
            .filter(status="SCHEDULED")
            .select_related(
                "job",
                "applicant",
            )[:10]
        )

        context["recent_jobs"] = (
            Job.objects
            .select_related(
                "company",
                "title",
                "location",
            )
            .order_by("-created_at")[:10]
        )

        return context


# ==========================================================
# JOB LIST
# ==========================================================

class JobListView(LoginRequiredMixin, ListView):

    model = Job

    template_name = "jobs/job/list.html"

    context_object_name = "jobs"

    paginate_by = 20

    def get_queryset(self):

        queryset = (
            Job.objects
            .select_related(
                "company",
                "title",
                "category",
                "industry",
                "location",
            )
            .prefetch_related(
                "skills",
                "benefits",
            )
            .annotate(
                applicant_count=Count("applicants")
            )
        )

        self.filterset = JobFilter(
            self.request.GET,
            queryset=queryset,
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["filter"] = self.filterset

        return context


# ==========================================================
# JOB DETAIL
# ==========================================================

class JobDetailView(LoginRequiredMixin, DetailView):

    model = Job

    template_name = "jobs/job/detail.html"

    context_object_name = "job"

    queryset = (
        Job.objects
        .select_related(
            "company",
            "title",
            "category",
            "industry",
            "location",
        )
        .prefetch_related(
            "skills",
            "benefits",
            "languages",
            "assets",
            "documents",
        )
    )


# ==========================================================
# JOB CREATE
# ==========================================================

class JobCreateView(LoginRequiredMixin, CreateView):

    model = Job

    form_class = JobForm

    template_name = "jobs/job/form.html"

    success_url = reverse_lazy("job_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Job created successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# JOB UPDATE
# ==========================================================

class JobUpdateView(LoginRequiredMixin, UpdateView):

    model = Job

    form_class = JobForm

    template_name = "jobs/job/form.html"

    success_url = reverse_lazy("job_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Job updated successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# JOB DELETE
# ==========================================================

class JobDeleteView(LoginRequiredMixin, DeleteView):

    model = Job

    template_name = "jobs/job/delete.html"

    success_url = reverse_lazy("job_list")

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Job deleted successfully.",
        )

        return super().delete(request, *args, **kwargs)



from django.http import JsonResponse
from django.db.models import Count


# ==========================================================
# APPLICANT LIST
# ==========================================================

class JobApplicantListView(LoginRequiredMixin, ListView):

    model = JobApplicant

    template_name = "jobs/applicant/list.html"

    context_object_name = "applicants"

    paginate_by = 20

    def get_queryset(self):

        queryset = (
            JobApplicant.objects
            .select_related(
                "job",
                "location",
                "postal_code",
            )
            .prefetch_related(
                "interviews",
            )
            .annotate(
                interview_count=Count("interviews")
            )
            .order_by("-applied_at")
        )

        self.filterset = JobApplicantFilter(
            self.request.GET,
            queryset=queryset,
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["filter"] = self.filterset

        return context


# ==========================================================
# APPLICANT DETAIL
# ==========================================================

class JobApplicantDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = JobApplicant

    context_object_name = "applicant"

    template_name = "jobs/applicant/detail.html"

    queryset = (
        JobApplicant.objects
        .select_related(
            "job",
            "location",
            "postal_code",
        )
        .prefetch_related(
            "interviews",
            "activities",
        )
    )


# ==========================================================
# APPLICANT CREATE
# ==========================================================

class JobApplicantCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = JobApplicant

    form_class = JobApplicantForm

    template_name = "jobs/applicant/form.html"

    success_url = reverse_lazy(
        "job_applicant_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Applicant added successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# APPLICANT UPDATE
# ==========================================================

class JobApplicantUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = JobApplicant

    form_class = JobApplicantForm

    template_name = "jobs/applicant/form.html"

    success_url = reverse_lazy(
        "job_applicant_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Applicant updated successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# APPLICANT DELETE
# ==========================================================

class JobApplicantDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = JobApplicant

    template_name = "jobs/applicant/delete.html"

    success_url = reverse_lazy(
        "job_applicant_list"
    )

    def delete(
        self,
        request,
        *args,
        **kwargs,
    ):

        messages.success(
            request,
            "Applicant deleted successfully.",
        )

        return super().delete(
            request,
            *args,
            **kwargs,
        )


# ==========================================================
# CHANGE STATUS
# ==========================================================

class ApplicantStatusUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = JobApplicant

    fields = ["status"]

    http_method_names = [
        "post",
    ]

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        applicant = self.get_object()

        applicant.status = request.POST.get(
            "status"
        )

        applicant.save(
            update_fields=[
                "status",
            ]
        )

        return JsonResponse(
            {
                "success": True,
                "status": applicant.status,
            }
        )


# ==========================================================
# SHORTLIST
# ==========================================================

class ApplicantShortlistView(
    LoginRequiredMixin,
    UpdateView,
):

    model = JobApplicant

    http_method_names = ["post"]

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        applicant = self.get_object()

        applicant.status = (
            ApplicationStatus.SHORTLISTED
        )

        applicant.save(
            update_fields=["status"]
        )

        return JsonResponse(
            {
                "success": True,
            }
        )


# ==========================================================
# REJECT
# ==========================================================

class ApplicantRejectView(
    LoginRequiredMixin,
    UpdateView,
):

    model = JobApplicant

    http_method_names = ["post"]

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        applicant = self.get_object()

        applicant.status = (
            ApplicationStatus.REJECTED
        )

        applicant.save(
            update_fields=["status"]
        )

        return JsonResponse(
            {
                "success": True,
            }
        )

from django.views import View
from django.http import JsonResponse


# ==========================================================
# INTERVIEW LIST
# ==========================================================

class InterviewScheduleListView(
    LoginRequiredMixin,
    ListView,
):

    model = InterviewSchedule

    template_name = "jobs/interview/list.html"

    context_object_name = "interviews"

    paginate_by = 20

    def get_queryset(self):

        return (
            InterviewSchedule.objects
            .select_related(
                "job",
                "applicant",
            )
            .order_by(
                "-scheduled_datetime",
            )
        )


# ==========================================================
# INTERVIEW CREATE
# ==========================================================

class InterviewScheduleCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = InterviewSchedule

    form_class = InterviewScheduleForm

    template_name = "jobs/interview/form.html"

    success_url = reverse_lazy(
        "interview_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Interview scheduled successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# INTERVIEW UPDATE
# ==========================================================

class InterviewScheduleUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = InterviewSchedule

    form_class = InterviewScheduleForm

    template_name = "jobs/interview/form.html"

    success_url = reverse_lazy(
        "interview_list"
    )


# ==========================================================
# INTERVIEW DELETE
# ==========================================================

class InterviewScheduleDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = InterviewSchedule

    template_name = "jobs/interview/delete.html"

    success_url = reverse_lazy(
        "interview_list"
    )


# ==========================================================
# OFFER LIST
# ==========================================================

class OfferLetterListView(
    LoginRequiredMixin,
    ListView,
):

    model = OfferLetter

    template_name = "jobs/offer/list.html"

    context_object_name = "offers"

    paginate_by = 20

    queryset = (
        OfferLetter.objects
        .select_related(
            "job",
            "applicant",
            "work_location",
        )
        .order_by("-offer_date")
    )


# ==========================================================
# OFFER CREATE
# ==========================================================

class OfferLetterCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = OfferLetter

    form_class = OfferLetterForm

    template_name = "jobs/offer/form.html"

    success_url = reverse_lazy(
        "offer_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Offer generated successfully.",
        )

        return super().form_valid(form)


# ==========================================================
# OFFER UPDATE
# ==========================================================

class OfferLetterUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = OfferLetter

    form_class = OfferLetterForm

    template_name = "jobs/offer/form.html"

    success_url = reverse_lazy(
        "offer_list"
    )


# ==========================================================
# OFFER DELETE
# ==========================================================

class OfferLetterDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = OfferLetter

    template_name = "jobs/offer/delete.html"

    success_url = reverse_lazy(
        "offer_list"
    )


# ==========================================================
# EMPLOYEE JOINING LIST
# ==========================================================

class EmployeeJoiningListView(
    LoginRequiredMixin,
    ListView,
):

    model = EmployeeJoining

    template_name = "jobs/joining/list.html"

    context_object_name = "employees"

    paginate_by = 20

    queryset = (
        EmployeeJoining.objects
        .select_related(
            "applicant",
            "offer_letter",
            "work_location",
        )
        .order_by("-joining_date")
    )


# ==========================================================
# EMPLOYEE JOINING CREATE
# ==========================================================

class EmployeeJoiningCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = EmployeeJoining

    form_class = EmployeeJoiningForm

    template_name = "jobs/joining/form.html"

    success_url = reverse_lazy(
        "joining_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Employee joining completed.",
        )

        return super().form_valid(form)


# ==========================================================
# EMPLOYEE JOINING UPDATE
# ==========================================================

class EmployeeJoiningUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = EmployeeJoining

    form_class = EmployeeJoiningForm

    template_name = "jobs/joining/form.html"

    success_url = reverse_lazy(
        "joining_list"
    )


# ==========================================================
# EMPLOYEE JOINING DELETE
# ==========================================================

class EmployeeJoiningDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = EmployeeJoining

    template_name = "jobs/joining/delete.html"

    success_url = reverse_lazy(
        "joining_list"
    )


# ==========================================================
# DASHBOARD AJAX COUNTS
# ==========================================================

class DashboardStatsView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        data = {

            "jobs": Job.objects.count(),

            "active_jobs": Job.objects.filter(
                status="ACTIVE"
            ).count(),

            "applicants": JobApplicant.objects.count(),

            "selected": JobApplicant.objects.filter(
                status="SELECTED"
            ).count(),

            "interviews": InterviewSchedule.objects.count(),

            "offers": OfferLetter.objects.count(),

            "joined": EmployeeJoining.objects.count(),

        }

        return JsonResponse(data)