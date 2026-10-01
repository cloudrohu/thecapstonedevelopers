import uuid

from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from apps.properties.models import Project

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_created",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_updated",
    )

    class Meta:
        abstract = True


class Setting(BaseModel):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )

    site_name = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    favicon = models.ImageField(upload_to="settings/", blank=True, null=True)
    offer_img = models.ImageField(upload_to="settings/", blank=True, null=True)
    search_bg = models.ImageField(upload_to="settings/", blank=True, null=True)
    Virtual_bg = models.ImageField(upload_to="settings/", blank=True, null=True)
    header_footer_color = models.CharField(max_length=150, blank=True, null=True)
    text_color = models.CharField(max_length=150, blank=True, null=True)
    button_color = models.CharField(max_length=150, blank=True, null=True)
    rera_color = models.CharField(max_length=150, blank=True, null=True)
    rera_number = models.CharField(max_length=150, blank=True, null=True)
    current_project_rera = models.CharField(max_length=150, blank=True, null=True)
    virtual_360_url = models.TextField(blank=True, null=True, )
    virtual_360_title = models.CharField(max_length=200, blank=True, null=True, default="360° Airspace Panorama",help_text="Heading/Title for 360 Section")
    googletagmanager = models.CharField(max_length=150, blank=True, null=True)
    google_label = models.CharField(max_length=150, blank=True, null=True)
    google_map = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    linkexplore = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    smtpserver = models.CharField(max_length=100, blank=True, null=True)
    smtpemail = models.EmailField(max_length=100, blank=True, null=True)
    smtppassword = models.CharField(max_length=100, blank=True, null=True)
    smtpport = models.CharField(max_length=10, blank=True, null=True)
    working_days = models.CharField(max_length=100, blank=True, null=True, help_text="Example: Mon - Sun")
    working_hours = models.CharField(max_length=100, blank=True, null=True, help_text="Example: 10:00 AM - 6:00 PM")
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    footer_text = models.CharField(max_length=250, blank=True, null=True)
    copy_right = models.CharField(max_length=100, blank=True, null=True)
    privacy_policy_title = models.CharField(max_length=200, blank=True, null=True)
    privacy_policy_content = CKEditor5Field(blank=True, null=True)
    disclaimer_title = models.CharField(max_length=200, blank=True, null=True)
    disclaimer_content = CKEditor5Field(blank=True, null=True)
    terms_conditions = CKEditor5Field(blank=True, null=True)
    disclaimer = CKEditor5Field(blank=True, null=True)
    cookies = CKEditor5Field(blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="True", blank=True, null=True)

    class Meta:
        verbose_name = "Website Setting"
        verbose_name_plural = "0. Website Settings"

    def __str__(self):
        return self.site_name or ""

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="100" style="object-fit:contain;border-radius:6px;">')
        return "No Logo"

    logo_tag.short_description = "Logo"



class Slider(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="sliders", blank=True, null=True)

    title1 = models.CharField(max_length=200, blank=True, null=True)
    title2 = models.CharField(max_length=300, blank=True, null=True)
    badge_title = models.CharField(max_length=300, blank=True, null=True)
    descriptions = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to="hero/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Slider"
        verbose_name_plural = "1. Sliders"

    def __str__(self):
        return self.title1 or ""


class About(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="about_sections", blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    content = CKEditor5Field(blank=True, null=True)
    read_legacy = CKEditor5Field(blank=True, null=True)
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    about_title = models.CharField(max_length=200, blank=True, null=True)
    about_subtitle = models.CharField(max_length=300, blank=True, null=True)
    about_content = CKEditor5Field(blank=True, null=True)
    mission_title = models.CharField(max_length=200, blank=True, null=True)
    mission_content = CKEditor5Field(blank=True, null=True)
    vision_title = models.CharField(max_length=200, blank=True, null=True)
    vision_content = CKEditor5Field(blank=True, null=True)
    hero_title = models.CharField(max_length=250, blank=True, null=True)
    hero_highlight = models.CharField(max_length=150, blank=True, null=True)
    hero_subtitle = models.CharField(max_length=200, blank=True, null=True)
    hero_description = CKEditor5Field(blank=True, null=True)
    hero_background = models.ImageField(upload_to="about/hero/", blank=True, null=True)
    button_one_text = models.CharField(max_length=50, default="Explore Legacy", blank=True, null=True)
    button_one_link = models.CharField(max_length=255, blank=True, null=True)
    button_two_text = models.CharField(max_length=50, default="View Projects", blank=True, null=True)
    button_two_link = models.CharField(max_length=255, blank=True, null=True)
    seo_title = models.CharField(max_length=200, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    right_image1 = models.ImageField(upload_to="about/", blank=True, null=True)
    right_image2 = models.ImageField(upload_to="about/", blank=True, null=True)
    years_of_experience = models.CharField(max_length=100, blank=True, null=True)
    happy_families = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "2. About Section"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or ""


class Contact_Page(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="contact_pages", blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    sub_heading = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    map_iframe = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "3. Contact Pages"

    def __str__(self):
        return self.heading or ""


class Our_Team(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="team_members", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "4. Our Team"

    def __str__(self):
        return self.name or ""


class Testimonial(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="testimonials", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="testimonial/", blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, blank=True, null=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "5. Testimonials"

    def __str__(self):
        return f"{self.name or ''} ({self.rating or 0}⭐)"


class Why_Choose(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="why_choose_items", blank=True, null=True)
    icons = models.CharField(max_length=100, blank=True, null=True, help_text="Example: fa-solid fa-star")
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why Choose"
        verbose_name_plural = "6. Why Choose Us"

    def __str__(self):
        return self.title or ""


class USP(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="usp_item", blank=True, null=True)
    icons = models.CharField(max_length=100, blank=True, null=True, help_text="Example: fa-solid fa-star")
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title or ""


class FAQ(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="faqs", blank=True, null=True)
    question = models.CharField(max_length=300, blank=True, null=True)
    answer = CKEditor5Field(blank=True, null=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "7. FAQs"

    def __str__(self):
        return self.question or ""


class ImpactMetric(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="impact_metrics", blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True, help_text='Example: "10,000+" or "95%"')
    icon = models.CharField(max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Impact Metric"
        verbose_name_plural = "8. Impact Metrics"

    def __str__(self):
        return f"{self.title or ''}: {self.value or ''}"


class Gallery(BaseModel):
    GALLERY_CHOICES = [
        ("project", "Projects"),
        ("events", "Events"),
        ("awards", "Awards"),
        ("amenities", "Amenities"),
        ("construction", "Construction"),
        ("interior", "Interior"),
        ("exterior", "Exterior"),
    ]

    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="gallery_items", blank=True, null=True)
    gallery_category = models.CharField(max_length=25, choices=GALLERY_CHOICES, default="project", blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Gallery"
        verbose_name_plural = "9. Gallery"

    def __str__(self):
        return self.title or ""


class Enquiry(BaseModel):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="enquiries", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(max_length=5000, blank=True, null=True)

    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "10. Enquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name or 'Unknown'} - {self.phone or 'No Phone'}"

class Inquiry(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="inquiries")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

class PriceBreakupInquiry(models.Model):
    project = models.ForeignKey(Project,on_delete=models.SET_NULL,null=True,blank=True,related_name="price_breakup_inquiries")

    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)

    property_type = models.CharField(max_length=100,blank=True,null=True)
    property_area = models.CharField(max_length=100,blank=True,null=True)
    property_price = models.CharField(max_length=100,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

