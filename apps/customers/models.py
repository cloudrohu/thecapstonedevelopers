from django.db import models

from apps.core.models import BaseModel

from apps.utility.models import Location, PostalCode
from apps.accounts.models import User
from apps.companies.models import Company


# ==========================================================
# MASTER TABLES
# ==========================================================

class CustomerCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CustomerSource(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CustomerRequirement(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# CUSTOMER
# ==========================================================

class Customer(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers"
    )

    category = models.ForeignKey(
        CustomerCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    source = models.ForeignKey(
        CustomerSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    requirement = models.ForeignKey(
        CustomerRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=20)

    alternate_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    website = models.URLField(blank=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    address = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_customers"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


# ==========================================================
# CUSTOMER CONTACT
# ==========================================================

class CustomerContact(BaseModel):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    name = models.CharField(max_length=150)

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# CUSTOMER DOCUMENT
# ==========================================================

class CustomerDocument(BaseModel):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="customers/documents/"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title