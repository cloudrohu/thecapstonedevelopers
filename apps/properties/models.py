from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from apps.core.models import BaseModel
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from apps.utility.models.location import Location, LocationType,PostalCode
from apps.properties_utility.models import PossessionIn,PropertyType,ProjectAmenities,Bank
from multiselectfield import MultiSelectField
from embed_video.fields import EmbedVideoField
from apps.properties_utility.compress_mixin import ImageCompressionMixin
from django.db.models import Min, Max
from django.utils import timezone
import re

def get_crm_id(obj):
    """
    Generate readable CRM ID based on model type.
    Example:
    Developer -> DEV3514
    Architect -> ARC193
    Engineer  -> ENG105
    Project   -> PRO221
    """

    if isinstance(obj, Developer):
        prefix = "DEV"

    elif isinstance(obj, Architects):
        prefix = "ARC"

    elif isinstance(obj, Engineer):
        prefix = "ENG"

    elif isinstance(obj, Project):
        prefix = "PRO"

    else:
        return str(obj.pk)

    return f"{prefix}{obj.pk}"

def refresh_calling_status(obj):

    if isinstance(obj, Developer):
        field = "developer"

    elif isinstance(obj, Architects):
        field = "architect"

    elif isinstance(obj, Engineer):
        field = "engineer"

    elif isinstance(obj, Project):
        field = "project"

    else:
        return

    has_meeting = Meeting.objects.filter(
        **{field: obj}
    ).exists()

    has_followup = Followup.objects.filter(
        **{field: obj}
    ).exists()

    meeting_done = Meeting.objects.filter(
        **{
            field: obj,
            "status": "Deal Done",
        }
    ).exists()

    followup_done = Followup.objects.filter(
        **{
            field: obj,
            "status": "Deal Done",
        }
    ).exists()

    if meeting_done or followup_done:
        status = "Deal Done"

    elif has_meeting and has_followup:
        status = "Meeting_FollowUp"

    elif has_meeting:
        status = "Meeting"

    elif has_followup:
        status = "FollowUp"

    else:
        status = "New"

    if obj.calling_status != status:
        obj.calling_status = status
        obj.save(update_fields=["calling_status"])


def refresh_parent_status(obj):

        if obj.developer:
            obj.developer.refresh_calling_status()

        if obj.architect:
            obj.architect.refresh_calling_status()

        if obj.engineer:
            obj.engineer.refresh_calling_status()

        if obj.project:
            obj.project.refresh_calling_status()


def format_price(value):
    """
    Convert rupees into Indian readable format.
    Examples:
    85000      -> ₹85,000
    550000     -> ₹5.50 L
    25000000   -> ₹2.50 Cr
    """

    if value in (None, "", 0):
        return ""

    try:
        value = int(value)
    except (TypeError, ValueError):
        return ""

    if value >= 10000000:
        return f"₹{value / 10000000:.2f} Cr"

    if value >= 100000:
        return f"₹{value / 100000:.2f} L"

    return f"₹{value:,}"

def format_price_range(price_min, price_max):
    """
    Example:
    4500000, 7500000
    -> ₹45.00 L – ₹75.00 L

    25000000, 32000000
    -> ₹2.50 Cr – ₹3.20 Cr
    """

    if not price_min and not price_max:
        return "Price on Request"

    if price_min is None:
        return format_price(price_max)

    if price_max is None:
        return format_price(price_min)

    if price_min == price_max:
        return format_price(price_min)

    return f"{format_price(price_min)} – {format_price(price_max)}"

def clean_phone_last10(phone: str):
    if not phone:
        return None

    digits = re.sub(r"\D", "", str(phone))
    return digits[-10:] if len(digits) >= 10 else digits




class Developer(BaseModel):

    CALLING_STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("Deal Done", "Deal Done"),
    ]

    title = models.CharField(max_length=150,unique=True,)

    city = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="developers_city",limit_choices_to={"location_type": LocationType.DISTRICT_CITY},null=True,blank=True,)

    locality = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="developer_locality",limit_choices_to={"location_type": LocationType.LOCALITY_AREA},null=True,blank=True,)

    area = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="developer_area",limit_choices_to={"location_type": LocationType.SUBLOCALITY_AREA},null=True,blank=True,)

    postal_code = models.ForeignKey(PostalCode,on_delete=models.PROTECT,related_name="developers",null=True,blank=True,)

    address = models.TextField(blank=True,null=True,)

    contact_person = models.CharField(max_length=255,blank=True,null=True,)

    contact_no = models.CharField(max_length=20,blank=True,null=True,)

    email = models.EmailField(blank=True,null=True,)

    google_map = models.URLField(max_length=1000,blank=True,null=True,)

    web_site = models.URLField(max_length=300,blank=True,null=True,)

    keywords = models.CharField(max_length=255,blank=True,null=True,)

    about_developer = models.TextField(blank=True,null=True,)


    read_more = CKEditor5Field(blank=True, null=True)


    note = models.TextField(blank=True,null=True,)

    logo = models.ImageField(upload_to="developer/logo/",blank=True,null=True,)

    featured_builder = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    calling_status = models.CharField(max_length=25,choices=CALLING_STATUS_CHOICES,default="New",blank=True,null=True,)

    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="developer_assigned",blank=True,null=True,)

    slug = models.SlugField(max_length=500,unique=True,blank=True,null=True,)

    id = models.CharField(primary_key=True,max_length=20,editable=False,)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Developer"
        verbose_name_plural = "1. Developers"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # -------------------------
        # CLEAN PHONE NUMBER
        # -------------------------
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        # -------------------------
        # GENERATE DEVELOPER ID
        # DEV000001
        # DEV000002
        # DEV000003
        # -------------------------
        if not self.id:

            last_developer = (
                Developer.objects
                .filter(id__startswith="DEV")
                .order_by("-id")
                .first()
            )

            if last_developer and last_developer.id:
                last_number = int(
                    last_developer.id.replace("DEV", "")
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.id = f"DEV{next_number:06d}"

        # -------------------------
        # SLUG
        # -------------------------
        if not self.slug:
            self.slug = slugify(self.title)

        # -------------------------
        # SAVE
        # -------------------------
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            "developer_detail",
            kwargs={"slug": self.slug},
        )


    def logo_preview(self):
        if self.logo:
            return mark_safe(
                f'<img src="{self.logo.url}" width="60" style="border-radius:6px;" />'
            )
        return "No Image"


    logo_preview.short_description = "Logo"


    def refresh_calling_status(self):
        refresh_calling_status(self)


class DeveloperImpactMetric(BaseModel):

    setting = models.ForeignKey(Developer,on_delete=models.CASCADE,related_name="developer_impact_metrics",blank=True,null=True,verbose_name="Developer",)

    title = models.CharField(max_length=255,blank=True,null=True,verbose_name="Metric Title",help_text='Example: "Completed Projects"',)

    value = models.CharField(max_length=100,blank=True,null=True,verbose_name="Metric Value",help_text='Example: "25+", "10,000+" or "95%"',)

    icon = models.CharField(max_length=500,blank=True,null=True,verbose_name="Font Awesome Icon",help_text='Example: "fa-solid fa-building"',)

    order = models.PositiveIntegerField(default=0,blank=True,null=True,verbose_name="Display Order",)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Impact Metric"
        verbose_name_plural = "Developer Impact Metrics"

    def __str__(self):
        return f"{self.title or 'Metric'}: {self.value or 'N/A'}"



class Architects(BaseModel):

    CALLING_STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("Deal Done", "Deal Done"),
    ]

    title = models.CharField(
        max_length=150,
        unique=True,
    )

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="architects_city",
        limit_choices_to={"location_type": LocationType.DISTRICT_CITY},
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="architects_locality",
        limit_choices_to={"location_type": LocationType.LOCALITY_AREA},
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="architects_area",
        limit_choices_to={"location_type": LocationType.SUBLOCALITY_AREA},
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="architects",
        null=True,
        blank=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    contact_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    google_map = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
    )

    web_site = models.URLField(
        max_length=300,
        blank=True,
        null=True,
    )

    keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    about_architect = models.TextField(
        blank=True,
        null=True,
    )

    note = models.TextField(
        blank=True,
        null=True,
    )

    logo = models.ImageField(
        upload_to="architect/logo/",
        blank=True,
        null=True,
    )

    featured_architect = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    is_featured = models.BooleanField(default=False)

    calling_status = models.CharField(
        max_length=25,
        choices=CALLING_STATUS_CHOICES,
        default="New",
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="architect_assigned",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Architect"
        verbose_name_plural = "2. Architects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = f"{slugify(self.title)}-{self.pk}"
            super().save(update_fields=["slug"])

    def get_absolute_url(self):
        return reverse(
            "architect_detail",
            kwargs={"slug": self.slug},
        )

    def logo_preview(self):
        if self.logo:
            return mark_safe(
                f'<img src="{self.logo.url}" width="60" style="border-radius:6px;" />'
            )
        return "No Image"

    logo_preview.short_description = "Logo"

    def refresh_calling_status(self):
        refresh_calling_status(self)



class Engineer(BaseModel):

    CALLING_STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("Deal Done", "Deal Done"),
    ]

    title = models.CharField(
        max_length=150,
        unique=True,
    )

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="engineers_city",
        limit_choices_to={"location_type": LocationType.DISTRICT_CITY},
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="engineers_locality",
        limit_choices_to={"location_type": LocationType.LOCALITY_AREA},
        null=True,
        blank=True,
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="engineers_area",
        limit_choices_to={"location_type": LocationType.SUBLOCALITY_AREA},
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="engineers",
        null=True,
        blank=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    contact_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    google_map = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
    )

    web_site = models.URLField(
        max_length=300,
        blank=True,
        null=True,
    )

    keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    about_engineer = models.TextField(
        blank=True,
        null=True,
    )

    note = models.TextField(
        blank=True,
        null=True,
    )

    logo = models.ImageField(
        upload_to="engineer/logo/",
        blank=True,
        null=True,
    )

    featured_engineer = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    is_featured = models.BooleanField(default=False)

    calling_status = models.CharField(
        max_length=25,
        choices=CALLING_STATUS_CHOICES,
        default="New",
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="engineer_assigned",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Engineer"
        verbose_name_plural = "3. Engineers"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.slug:
            self.slug = f"{slugify(self.title)}-{self.pk}"
            super().save(update_fields=["slug"])

    def get_absolute_url(self):
        return reverse(
            "engineer_detail",
            kwargs={"slug": self.slug},
        )

    def logo_preview(self):
        if self.logo:
            return mark_safe(
                f'<img src="{self.logo.url}" width="60" style="border-radius:6px;" />'
            )
        return "No Image"

    logo_preview.short_description = "Logo"
    def refresh_calling_status(self):
        refresh_calling_status(self)


class Project(MPTTModel, BaseModel):
    
    CALLING_STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("FollowUp", "Follow Up"),
        ("Meeting_FollowUp", "Meeting-Follow Up"),
        ("Not Received", "Not Received"),
        ("Not Interested", "Not Interested"),
        ("Deal Done", "Deal Done"),
    ]

    BHK_CHOICES = (
        ('1 BHK', '1 BHK'), ('2 BHK', '2 BHK'), ('3 BHK', '3 BHK'), ('4 BHK', '4 BHK'),('5 BHK', '5 BHK'), 
        ('6 BHK', '6 BHK'), ('7 BHK', '7 BHK'), ('8 BHK', '8 BHK'), ('9 BHK', '9 BHK'),
        ('10 BHK', '10 BHK'), ('10+ BHK', '10+ BHK'),
    )

    CONSTRUCTION_STATUS_CHOICES = (
        ('Under Construction', 'Under Construction'), ('New Launch', 'New Launch'),
        ('Partially Ready To Move', 'Partially Ready To Move'), ('Ready To Move', 'Ready To Move'),
        ('Deleverd', 'Deleverd'),
    )
    
    MONTH_CHOICES = [
        ('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), 
        ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'),
        ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'),
    ]
    
    OCCUPANCY_CERTIFICATE_CHOICES = (('Yes', 'Yes'),('No', 'No'), )
    COMMENCEMENT_CERTIFICATE_CHOICES = (('Yes', 'Yes'),('No', 'No'),)
    
    calling_status = models.CharField(
        max_length=25,
        choices=CALLING_STATUS_CHOICES,
        default="New",
        null=True,
        blank=True,
    )

    # --- Project Core Fields ---
    occupancy_certificate = models.CharField(max_length=25, choices=OCCUPANCY_CERTIFICATE_CHOICES,null=True, blank=True)
    commencement_certificate = models.CharField(max_length=25, choices=COMMENCEMENT_CERTIFICATE_CHOICES,null=True, blank=True)
    
    construction_status = models.CharField(max_length=25, choices=CONSTRUCTION_STATUS_CHOICES)
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name="projects",
    )

    # MPTT Hierarchy
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=250)
    
    # Foreign Keys
    developer = models.ForeignKey(
        Developer,
        on_delete=models.PROTECT,
        related_name="projects",
    )
    architect = models.ForeignKey(
        Architects,
        on_delete=models.PROTECT,
        related_name="projects",
        blank=True,
        null=True,
    )
    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.PROTECT,
        related_name="projects",
        blank=True,
        null=True,
)
    
    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="project_city",
        limit_choices_to={"location_type": LocationType.DISTRICT_CITY},
        null=True,
        blank=True,
    )
    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="projects_locality",
        limit_choices_to={"location_type": LocationType.LOCALITY_AREA},
        null=True,
        blank=True,
    )
    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="projects_area",
        limit_choices_to={"location_type": LocationType.SUBLOCALITY_AREA},
        null=True,
        blank=True,
    )
    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="projects",
        null=True,
        blank=True,
    )
    address = models.TextField(
        blank=True,
        null=True,
    )
    
    land_parcel = models.CharField(max_length=50,null=True, blank=True)
    bhk_type = MultiSelectField(choices=BHK_CHOICES, max_length=50,null=True, blank=True)
    floor = models.CharField(max_length=50,null=True, blank=True)
    
    possession_year = models.ForeignKey(PossessionIn, on_delete=models.PROTECT,null=True, blank=True) 
    possession_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True, help_text="Select Possession Month")
    
    luxurious = models.CharField(max_length=50,null=True, blank=True)
    pricing = models.CharField(max_length=50,null=True, blank=True) 
    youtube_embed_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="YouTube Video ID"
    )
    
    featured_property = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )
    google_map_iframe = models.TextField(
        blank=True,
        null=True,
    )
    id = models.CharField(
        primary_key=True,
        max_length=20,
        editable=False,
    )
    slug = models.SlugField(unique=True, null=True, blank=True,max_length=555,)


    # --- Overridden Methods ---
    def __str__(self):
        # Uses MPTT logic for full path (e.g., Phase 1 / Block A)
        full_path = [str(node.project_name) for node in self.get_ancestors(include_self=True)]
        return ' / '.join(full_path)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "4. Projects"
    
        # models.py
    def image_tag(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" height="60" />'
            )
        return "-"

    image_tag.short_description = "Image"

    def refresh_calling_status(self):
        refresh_calling_status(self)



    def save(self, *args, **kwargs):

        # ==========================================
        # GENERATE PROJECT ID FIRST
        # ==========================================
        if not self.id:

            last_project = (
                Project.objects
                .filter(id__startswith="PRO")
                .order_by("-id")
                .first()
            )

            if last_project and last_project.id:
                last_number = int(
                    last_project.id.replace("PRO", "")
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.id = f"PRO{next_number:06d}"

        # ==========================================
        # BHK SLUG
        # ==========================================
        bhk_slug = ""

        if self.bhk_type:

            bhk_values = self.bhk_type

            if isinstance(bhk_values, str):
                bhk_values = [
                    value.strip()
                    for value in bhk_values.split(",")
                    if value.strip()
                ]

            bhk_numbers = []

            for bhk in bhk_values:
                number = str(bhk).replace(" BHK", "").strip()
                bhk_numbers.append(number)

            if bhk_numbers:
                bhk_slug = f"{'-'.join(bhk_numbers)}-bhk"

        # ==========================================
        # PROPERTY TYPE
        # ==========================================
        property_type_slug = ""

        if self.property_type:
            property_type_slug = slugify(
                self.property_type.name
            )

        # ==========================================
        # LOCALITY
        # ==========================================
        locality_slug = ""

        if self.locality:
            locality_slug = slugify(
                self.locality.name
            )

        # ==========================================
        # CITY
        # ==========================================
        city_slug = ""

        if self.city:
            city_slug = slugify(
                self.city.name
            )

        # ==========================================
        # SEO SLUG
        # ==========================================
        slug_parts = [
            self.project_name,
            bhk_slug,
            property_type_slug,
            "in",
            locality_slug,
            city_slug,
        ]

        self.slug = slugify(
            "-".join(
                str(part).strip()
                for part in slug_parts
                if part
            )
        )

        # ==========================================
        # SAVE
        # ==========================================
        super().save(*args, **kwargs)


    
    class MPTTMeta:
        order_insertion_by = ['project_name']

    def get_absolute_url(self):
        return reverse("project_details", kwargs={'id': self.id, 'slug': self.slug})

    def get_configuration_details(self):
        from django.db.models import Min, Max

        configs = self.configurations.all()
        if not configs.exists():
            return ""

        summary_lines = []
        bhk_types = sorted(set(configs.values_list("bhk_type", flat=True)))

        for bhk in bhk_types:
            bhk_configs = configs.filter(bhk_type=bhk)

            # Area range
            area_min = bhk_configs.aggregate(Min("area_sqft"))["area_sqft__min"]
            area_max = bhk_configs.aggregate(Max("area_sqft"))["area_sqft__max"]
            area_range = f"{area_min}" if area_min == area_max else f"{area_min}-{area_max}"

            # Price range
            price_min = bhk_configs.aggregate(Min("price_in_rupees"))["price_in_rupees__min"]
            price_max = bhk_configs.aggregate(Max("price_in_rupees"))["price_in_rupees__max"]
            price_range = format_price_range(price_min, price_max)

            summary_lines.append(f"{bhk} {area_range} Sq.ft {price_range}")

        return "\n".join(summary_lines)


    def get_carpet_area_range(self):
        """
        Returns min-max carpet area from configurations
        Example: 761–1475 sqft
        """
        from django.db.models import Min, Max

        qs = self.configurations.all()
        if not qs.exists():
            return "NA"

        area_min = qs.aggregate(Min("area_sqft"))["area_sqft__min"]
        area_max = qs.aggregate(Max("area_sqft"))["area_sqft__max"]

        if area_min == area_max:
            return f"{area_min} sq.yd"

        return f"{area_min}–{area_max} sq.yd"

    def get_price_range(self):
        qs = self.configurations.all()

        if not qs.exists():
            return "Price on Request"

        price_min = qs.aggregate(Min("price_in_rupees"))["price_in_rupees__min"]
        price_max = qs.aggregate(Max("price_in_rupees"))["price_in_rupees__max"]

        def fmt(value):
            if value >= 10000000:
                return f"{value / 10000000:.2f} Cr"
            elif value >= 100000:
                return f"{value / 100000:.0f} L"
            return f"{value:,}"

        if price_min == price_max:
            return f"₹ {fmt(price_min)}"

        return f"₹ {fmt(price_min)} – {fmt(price_max)}"



class BookingOffer(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="BookingOffer")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
class WelcomeTo(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="welcomes")
    description = models.TextField(null=True, blank=True,max_length=5500)
    read_more= models.TextField(null=True, blank=True,max_length=5500)

    def __str__(self):
        return self.description
class WebSlider(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sliders")
    image = models.ImageField(upload_to='web_slider/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or f"Slider #{self.pk}"
class Overview(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="overviews")
    heading = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.heading
class AboutUs(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="aboutus")
    content = models.TextField()

    def __str__(self):
        return "About Us"
class USP(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="usps")
    point = models.CharField(null=True, blank=True,max_length=150)
    def __str__(self):
        return self.point


class Configuration(BaseModel):
    Project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="configurations")
    bhk_type = models.CharField(max_length=50)
    area_sqft = models.IntegerField(
        verbose_name="Area (Sq.ft)",
        help_text="Enter area in numeric square feet."
    ) 
    parking = models.BooleanField(default=False)
    unit_plan = models.ImageField(null=True, blank=True,upload_to='images/')

    
    # ✅ Sudhar 3: Price ko IntegerField banayein
    # Yeh lakh/crore calculations ke liye zaroori hai.
    price_in_rupees = models.IntegerField(
        verbose_name="Price (in ₹)",
        help_text="Enter price in total rupees (e.g., 5000000)."
    )

    def formatted_price(self):
        price = float(self.price_in_rupees)

        if price >= 10000000:
            crore = price / 10000000

            if crore == int(crore):
                return f"{int(crore)} Cr"

            return f"{crore:.2f}".rstrip("0").rstrip(".") + " Cr"

        elif price >= 100000:
            lakh = price / 100000

            if lakh == int(lakh):
                return f"{int(lakh)} Lakh"

            return f"{lakh:.2f}".rstrip("0").rstrip(".") + " Lakh"

        return f"{int(price):,}"

    def __str__(self):
        return f"{self.Project.project_name} - {self.bhk_type} ({self.area_sqft} sq.ft)"
    
    class Meta:
        # Configuration ke instances ko Project aur BHK type ke hisaab se arrange karein
        ordering = ['bhk_type']


class Connectivity(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="connectivity")
    title = models.CharField(max_length=150, help_text="e.g. Western Express Highway")
    subtitle = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. North-South Arterial Corridor")
    
    km = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 2.5 KM")

    drive_time = models.CharField(max_length=50, default="05 Mins", help_text="e.g. 04 Mins", blank=True, null=True,)
    metro_time = models.CharField(max_length=50, default="10 Mins", help_text="e.g. 08 Mins", blank=True, null=True,)
    walk_time = models.CharField(max_length=50, default="15 Mins", help_text="e.g. 20 Mins ya -- Mins", blank=True, null=True,)

    progress_percent = models.PositiveIntegerField(default=25, help_text="Telemetry progress bar width (1 - 100)")

    # Radar coordinates (Canvas par dot kahan dikhega)
    radar_radius = models.PositiveIntegerField(default=50, help_text="Center se doori (Value 25 se 120 ke beech rakhein)")
    radar_angle = models.FloatField(default=1.5, help_text="Angle in radians (0.1 se 6.2 ke beech)")

    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Connectivity Point"
        verbose_name_plural = "Connectivity Points"

    def __str__(self):
        return self.title
    

    
class Amenities(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="amenities")
    amenities = models.ForeignKey(ProjectAmenities, on_delete=models.CASCADE, related_name="amenities")
    
    def __str__(self):
        return f"{self.Project.project_name} - {self.amenities.title}"


    
class Gallery(BaseModel):
    CATEGORY_CHOICES = (
        ('all', 'All'),
        ('exterior', 'Exterior & Architecture'),
        ('interior', 'Luxury Interiors'),
        ('amenities', 'Amenities & Landscape'),
        ('construction', 'Construction Updates'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery")
    title = models.CharField(max_length=150, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='exterior')
    image = models.ImageField(upload_to="gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title or f"Gallery Item {self.id}"

    
class Header(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="headers")    
    title = models.CharField(max_length=2000,null=True, blank=True)
    keywords = models.CharField(max_length=2000,null=True, blank=True)
    meta_description = models.CharField(max_length=5000,null=True, blank=True)
    logo = models.ImageField(null=True, blank=True,upload_to='images/')
    welcome_to_bg = models.ImageField(null=True, blank=True,upload_to='headers/')
    virtual_site_visit_bg = models.ImageField(null=True, blank=True,upload_to='headers/')
    schedule_a_site_visit = models.ImageField(null=True, blank=True,upload_to='headers/')

    def __str__(self):
        return self.keywords
class RERA_Info(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rera")
    qr_image = models.ImageField(null=True, blank=True,upload_to='overviewimage/')
    registration_no = models.CharField(null=True, blank=True,max_length=50)
    project_registered = models.CharField(null=True, blank=True,max_length=50)
    government_rera_authorised_advertiser = models.CharField(null=True, blank=True,max_length=150)
    site_address  = models.CharField(null=True, blank=True,max_length=500)
    contact_us= models.CharField(null=True, blank=True,max_length=500)
    disclaimer= models.CharField(null=True, blank=True,max_length=1500)
    document = models.FileField(null=True, blank=True,upload_to='rera_docs/')

    def __str__(self):
        return self.registration_no
class WhyInvest(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="why_invest")
    title = models.CharField(max_length=350,null=True, blank=True)
    discripation = models.CharField(max_length=500,null=True, blank=True)
    

    def __str__(self):
        return f"Why Invest - {self.pk}"
class BankOffer(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bank_offers")
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="bank_offers")
    
    def __str__(self):
        return f"{self.Project.project_name} - {self.bank.title}"
class ProjectFAQ(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="faqs"
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.project_name} - {self.question}"
class Enquiry(BaseModel):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='enquiries'
    )
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    contacted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry for {self.project.project_name} by {self.name}"

    class Meta:
        verbose_name = 'Project Enquiry'
        verbose_name_plural = '3. Project Enquiries'
        ordering = ['-contacted_on']

class ProjectContactPerson(BaseModel):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contact_persons",
    )

    name = models.CharField(max_length=150)

    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Contact Person"
        verbose_name_plural = "Project Contact Persons"

    def __str__(self):
        return f"{self.project.project_name} - {self.name}"

class Comment(BaseModel):

    TYPE_CHOICES = (
        ("Developer", "Developer"),
        ("Architect", "Architect"),
        ("Engineer", "Engineer"),
        ("Project", "Project"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=True,
    )

    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )

    architect = models.ForeignKey(
        Architects,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )

    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        if self.project:
            return self.project.project_name

        if self.developer:
            return self.developer.title

        if self.architect:
            return self.architect.title

        if self.engineer:
            return self.engineer.title

        return "Comment"

    def clean(self):

        total = sum([
            bool(self.project),
            bool(self.developer),
            bool(self.architect),
            bool(self.engineer),
        ])

        if total == 0:
            raise ValidationError(
                "Please select Developer, Architect, Engineer or Project."
            )

        if total > 1:
            raise ValidationError(
                "Only one relation is allowed."
            )

    def save(self, *args, **kwargs):

        if self.project:
            self.type = "Project"

        elif self.developer:
            self.type = "Developer"

        elif self.architect:
            self.type = "Architect"

        elif self.engineer:
            self.type = "Engineer"

        self.full_clean()

        super().save(*args, **kwargs)

class VoiceRecording(BaseModel):

    TYPE_CHOICES = (
        ("Developer", "Developer"),
        ("Architect", "Architect"),
        ("Engineer", "Engineer"),
        ("Project", "Project"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=True,
    )

    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings",
    )

    architect = models.ForeignKey(
        Architects,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings",
    )

    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="voice_recordings",
    )

    file = models.FileField(
        upload_to="voice_recordings/",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_voice_uploaded",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Voice Recording"
        verbose_name_plural = "Voice Recordings"

    def __str__(self):

        if self.project:
            return f"{self.project.project_name} Voice"

        if self.developer:
            return f"{self.developer.title} Voice"

        if self.architect:
            return f"{self.architect.title} Voice"

        if self.engineer:
            return f"{self.engineer.title} Voice"

        return f"Voice {self.pk}"

    def clean(self):

        total = sum([
            bool(self.project),
            bool(self.developer),
            bool(self.architect),
            bool(self.engineer),
        ])

        if total == 0:
            raise ValidationError(
                "Please select Developer, Architect, Engineer or Project."
            )

        if total > 1:
            raise ValidationError(
                "Only one relation is allowed."
            )

    def save(self, *args, **kwargs):

        if self.project:
            self.type = "Project"

        elif self.developer:
            self.type = "Developer"

        elif self.architect:
            self.type = "Architect"

        elif self.engineer:
            self.type = "Engineer"

        self.full_clean()
        super().save(*args, **kwargs)

class Visit(BaseModel):

    TYPE_CHOICES = (
        ("Developer", "Developer"),
        ("Architect", "Architect"),
        ("Engineer", "Engineer"),
        ("Project", "Project"),
    )

    VISIT_FOR_CHOICES = (
        ("Meeting", "Meeting"),
        ("Door To Door", "Door To Door"),
        ("Site Visit", "Site Visit"),
        ("Follow Up", "Follow Up"),
        ("Negotiation", "Negotiation"),
    )

    VISIT_TYPE_CHOICES = (
        ("1st Visit", "1st Visit"),
        ("2nd Visit", "2nd Visit"),
        ("3rd Visit", "3rd Visit"),
        ("4th Visit", "4th Visit"),
        ("5th Visit", "5th Visit"),
    )

    VISIT_STATUS_CHOICES = (
        ("Meeting", "Meeting"),
        ("Interested", "Interested"),
        ("Follow Up", "Follow Up"),
        ("Deal Done", "Deal Done"),
        ("Not Interested", "Not Interested"),
        ("Owner Not Available", "Owner Not Available"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=True,
    )

    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits",
    )

    architect = models.ForeignKey(
        Architects,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits",
    )

    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="visits",
    )

    visit_for = models.CharField(
        max_length=50,
        choices=VISIT_FOR_CHOICES,
    )

    visit_type = models.CharField(
        max_length=50,
        choices=VISIT_TYPE_CHOICES,
    )

    visit_status = models.CharField(
        max_length=50,
        choices=VISIT_STATUS_CHOICES,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Visit"
        verbose_name_plural = "Visits"

    def __str__(self):
        return f"Visit #{self.pk}"

    def clean(self):

        total = sum([
            bool(self.project),
            bool(self.developer),
            bool(self.architect),
            bool(self.engineer),
        ])

        if total == 0:
            raise ValidationError(
                "Please select Developer, Architect, Engineer or Project."
            )

        if total > 1:
            raise ValidationError(
                "Only one relation is allowed."
            )

    def save(self, *args, **kwargs):

        if self.project:
            self.type = "Project"

        elif self.developer:
            self.type = "Developer"

        elif self.architect:
            self.type = "Architect"

        elif self.engineer:
            self.type = "Engineer"

        self.full_clean()
        super().save(*args, **kwargs)


class Followup(BaseModel):

    TYPE_CHOICES = (
        ("Developer", "Developer"),
        ("Architect", "Architect"),
        ("Engineer", "Engineer"),
        ("Project", "Project"),
    )

    FOLLOWUP_STATUS_CHOICES = (
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=True,
    )

    developer = models.OneToOneField(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup",
    )

    architect = models.OneToOneField(
        Architects,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup",
    )

    engineer = models.OneToOneField(
        Engineer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup",
    )

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="followup",
    )

    status = models.CharField(
        max_length=25,
        choices=FOLLOWUP_STATUS_CHOICES,
        default="New Followup",
    )

    followup_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_followup_assigned",
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    id = models.CharField(
        primary_key=True,
        max_length=20,
        editable=False,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Followup"
        verbose_name_plural = "Followups"

    def __str__(self):
        return f"Followup #{self.id}"

    def clean(self):

        total = sum([
            bool(self.project),
            bool(self.developer),
            bool(self.architect),
            bool(self.engineer),
        ])

        if total == 0:
            raise ValidationError(
                "Please select Developer, Architect, Engineer or Project."
            )

        if total > 1:
            raise ValidationError(
                "Only one relation is allowed."
            )

    def save(self, *args, **kwargs):

        # -------------------------
        # GENERATE FOLLOWUP ID
        # FU000001
        # -------------------------
        if not self.id:

            last_followup = (
                Followup.objects
                .filter(id__startswith="FU")
                .order_by("-id")
                .first()
            )

            if last_followup and last_followup.id:
                last_number = int(
                    last_followup.id.replace("FU", "")
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.id = f"FU{next_number:06d}"

        # -------------------------
        # SET TYPE
        # -------------------------
        if self.project:
            self.type = "Project"

        elif self.developer:
            self.type = "Developer"

        elif self.architect:
            self.type = "Architect"

        elif self.engineer:
            self.type = "Engineer"

        self.full_clean()

        super().save(*args, **kwargs)

        # -------------------------
        # DEAL DONE
        # -------------------------
        if self.status == "Deal Done":

            if self.developer:
                Developer.objects.filter(
                    pk=self.developer_id
                ).update(calling_status="Deal Done")

            if self.architect:
                Architects.objects.filter(
                    pk=self.architect_id
                ).update(calling_status="Deal Done")

            if self.engineer:
                Engineer.objects.filter(
                    pk=self.engineer_id
                ).update(calling_status="Deal Done")

            if self.project:
                Project.objects.filter(
                    pk=self.project_id
                ).update(calling_status="Deal Done")

        else:
            refresh_parent_status(self)

    def delete(self, *args, **kwargs):

        developer = self.developer
        architect = self.architect
        engineer = self.engineer
        project = self.project

        super().delete(*args, **kwargs)

        if developer:
            developer.refresh_calling_status()

        if architect:
            architect.refresh_calling_status()

        if engineer:
            engineer.refresh_calling_status()

        if project:
            project.refresh_calling_status()


class Meeting(BaseModel):

    TYPE_CHOICES = (
        ("Developer", "Developer"),
        ("Architect", "Architect"),
        ("Engineer", "Engineer"),
        ("Project", "Project"),
    )

    MEETING_STATUS_CHOICES = (
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    )

    # -------------------------
    # CUSTOM MEETING ID
    # MEET000001
    # -------------------------
    id = models.CharField(
        primary_key=True,
        max_length=20,
        editable=False,
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        null=True,
    )

    developer = models.OneToOneField(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting",
    )

    architect = models.OneToOneField(
        Architects,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting",
    )

    engineer = models.OneToOneField(
        Engineer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting",
    )

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="meeting",
    )

    status = models.CharField(
        max_length=25,
        choices=MEETING_STATUS_CHOICES,
        default="New Meeting",
    )

    meeting_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_meeting_assigned",
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"

    def __str__(self):
        return f"Meeting #{self.id}"

    def clean(self):

        total = sum([
            bool(self.project),
            bool(self.developer),
            bool(self.architect),
            bool(self.engineer),
        ])

        if total == 0:
            raise ValidationError(
                "Please select Developer, Architect, Engineer or Project."
            )

        if total > 1:
            raise ValidationError(
                "Only one relation is allowed."
            )

    def save(self, *args, **kwargs):

        # -------------------------
        # GENERATE MEETING ID
        # MEET000001
        # -------------------------
        if not self.id:

            last_meeting = (
                Meeting.objects
                .filter(id__startswith="MT")
                .order_by("-id")
                .first()
            )

            if last_meeting and last_meeting.id:
                last_number = int(
                    last_meeting.id.replace("MT", "")
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.id = f"MT{next_number:06d}"

        # -------------------------
        # SET TYPE
        # -------------------------
        if self.project:
            self.type = "Project"

        elif self.developer:
            self.type = "Developer"

        elif self.architect:
            self.type = "Architect"

        elif self.engineer:
            self.type = "Engineer"

        self.full_clean()

        super().save(*args, **kwargs)

        # -------------------------
        # DEAL DONE
        # -------------------------
        if self.status == "Deal Done":

            if self.developer:
                Developer.objects.filter(
                    pk=self.developer_id
                ).update(calling_status="Deal Done")

            if self.architect:
                Architects.objects.filter(
                    pk=self.architect_id
                ).update(calling_status="Deal Done")

            if self.engineer:
                Engineer.objects.filter(
                    pk=self.engineer_id
                ).update(calling_status="Deal Done")

            if self.project:
                Project.objects.filter(
                    pk=self.project_id
                ).update(calling_status="Deal Done")

        else:
            refresh_parent_status(self)

    def delete(self, *args, **kwargs):

        developer = self.developer
        architect = self.architect
        engineer = self.engineer
        project = self.project

        super().delete(*args, **kwargs)

        if developer:
            developer.refresh_calling_status()

        if architect:
            architect.refresh_calling_status()

        if engineer:
            engineer.refresh_calling_status()

        if project:
            project.refresh_calling_status()