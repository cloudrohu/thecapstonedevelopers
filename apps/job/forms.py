from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Job,
    JobApplicant,
    InterviewSchedule,
    OfferLetter,
    EmployeeJoining,
    ApplicationStatus,
    InterviewType,
)


# ==========================================================
# BASE FORM
# ==========================================================

class BaseModelForm(forms.ModelForm):

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            css = (
                "form-control"
            )

            if isinstance(
                field.widget,
                forms.CheckboxInput,
            ):
                css = "form-check-input"

            field.widget.attrs.setdefault(
                "class",
                css,
            )

            field.widget.attrs.setdefault(
                "autocomplete",
                "off",
            )


# ==========================================================
# JOB FORM
# ==========================================================

class JobForm(BaseModelForm):

    class Meta:

        model = Job

        exclude = (
            "slug",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

    def clean(self):

        cleaned_data = super().clean()

        minimum_salary = cleaned_data.get("minimum_salary")
        maximum_salary = cleaned_data.get("maximum_salary")

        if (
            minimum_salary
            and maximum_salary
            and minimum_salary > maximum_salary
        ):
            raise ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

        minimum_experience = cleaned_data.get("minimum_experience")
        maximum_experience = cleaned_data.get("maximum_experience")

        if (
            minimum_experience
            and maximum_experience
            and minimum_experience > maximum_experience
        ):
            raise ValidationError(
                "Minimum experience cannot be greater than maximum experience."
            )

        return cleaned_data

# ==========================================================
# JOB APPLICANT FORM
# ==========================================================

class JobApplicantForm(BaseModelForm):

    class Meta:

        model = JobApplicant

        exclude = (
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "applied_at",
        )

        widgets = {
            "expected_joining_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean(self):

        cleaned = super().clean()

        current_salary = cleaned.get("current_salary")
        expected_salary = cleaned.get("expected_salary")

        if (
            current_salary
            and expected_salary
            and expected_salary < current_salary
        ):
            raise ValidationError(
                "Expected salary cannot be less than current salary."
            )

        return cleaned

# ==========================================================
# INTERVIEW SCHEDULE FORM
# ==========================================================

class InterviewScheduleForm(BaseModelForm):

    class Meta:

        model = InterviewSchedule

        exclude = (
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

        widgets = {
            "scheduled_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

    def clean(self):

        cleaned = super().clean()

        if cleaned.get("duration") and cleaned["duration"] <= 0:
            raise ValidationError(
                "Duration must be greater than zero."
            )

        return cleaned
# ==========================================================
# OFFER LETTER FORM
# ==========================================================

class OfferLetterForm(BaseModelForm):

    class Meta:

        model = OfferLetter

        exclude = (
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "sent_at",
            "accepted_at",
            "rejected_at",
        )

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "offer_date": forms.DateInput(attrs={"type": "date"}),
            "valid_till": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):

        cleaned = super().clean()

        offer_date = cleaned.get("offer_date")
        valid_till = cleaned.get("valid_till")
        joining_date = cleaned.get("joining_date")

        if offer_date and valid_till:

            if valid_till < offer_date:
                raise ValidationError(
                    "Offer validity cannot be before offer date."
                )

        if offer_date and joining_date:

            if joining_date < offer_date:
                raise ValidationError(
                    "Joining date cannot be before offer date."
                )

        annual_ctc = cleaned.get("annual_ctc")
        monthly_salary = cleaned.get("monthly_salary")

        if (
            annual_ctc
            and monthly_salary
            and monthly_salary > annual_ctc
        ):
            raise ValidationError(
                "Monthly salary cannot exceed annual CTC."
            )

        return cleaned


# ==========================================================
# EMPLOYEE JOINING FORM
# ==========================================================

class EmployeeJoiningForm(BaseModelForm):

    class Meta:

        model = EmployeeJoining

        exclude = (
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "confirmation_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_employee_code(self):

        employee_code = self.cleaned_data["employee_code"]

        return employee_code.strip().upper()

    def clean(self):

        cleaned = super().clean()

        joining_date = cleaned.get("joining_date")
        confirmation_date = cleaned.get("confirmation_date")

        if (
            joining_date
            and confirmation_date
            and confirmation_date < joining_date
        ):
            raise ValidationError(
                "Confirmation date cannot be before joining date."
            )

        return cleaned


# ==========================================================
# SEARCH FORM
# ==========================================================

class SearchForm(forms.Form):

    keyword = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "form-control",
            }
        ),
    )


# ==========================================================
# BULK STATUS UPDATE FORM
# ==========================================================

class BulkStatusUpdateForm(forms.Form):

    ids = forms.CharField(
        widget=forms.HiddenInput(),
    )

    status = forms.ChoiceField(
        choices=ApplicationStatus.choices,
    )


# ==========================================================
# BULK INTERVIEW FORM
# ==========================================================

class BulkInterviewForm(forms.Form):

    interview_type = forms.ChoiceField(
    choices=InterviewType.choices,
)

    scheduled_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        )
    )

    interviewer = forms.CharField(
        max_length=200,
    )

    meeting_link = forms.URLField(
        required=False,
    )

    office_address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
            }
        ),
    )

    def clean(self):

        cleaned = super().clean()

        if (
            not cleaned.get("meeting_link")
            and not cleaned.get("office_address")
        ):
            raise ValidationError(
                "Meeting link or office address is required."
            )

        return cleaned