from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey

from mptt.models import MPTTModel
from django.utils.text import slugify
from apps.utility.models.base import MasterBaseModel



class Find_Form(models.Model):    
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name_plural='1. Find_Form'

class Googlemap_Status(models.Model):    
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name_plural='4. Googlemap_Status'

class Call_Status(models.Model):
    title = models.CharField(max_length=500,blank=True, null=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='2. Call_Status'

class SocialSite(models.Model):
    title = models.CharField(max_length=50,unique=True)   
    code = models.CharField(max_length=50,unique=True,null=True , blank=True)   
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='3. SocialSite'

class Meeting_Followup_Type(models.Model):
    title = models.CharField(max_length=100,unique=True)    
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class RequirementType(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='4. Requirement_Type'

class Response_Status(models.Model):
    name = models.CharField(max_length=100,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural='5. Response_Status'

class PropertyType(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Parent Type/Category'
    )
    
    is_top_level = models.BooleanField(default=False) 
    
    is_selectable = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "Property Types"

    def __str__(self):
        full_path = [node.name for node in self.get_ancestors(include_self=True)]
        return ' / '.join(full_path)
    
class PossessionIn(models.Model):
    year = models.PositiveIntegerField(
        unique=True,
        help_text="e.g. 2025"
    )

    class Meta:
        verbose_name = "Possession Year"
        verbose_name_plural = "Possession Years"
        ordering = ['year']

    def __str__(self):
        return str(self.year)

class ProjectAmenities(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100,blank=True, null=True)
    
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title

class Bank(models.Model):
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='03. Bank'

class PropertyAmenities(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='property/amenities/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Property Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

    def icon_tag(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="40" height="40" />')
        return ""
    icon_tag.short_description = "Icon"




class UnitType(MasterBaseModel):
    class Meta:
        verbose_name = "Unit Type"
        verbose_name_plural = "Unit Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Furnishing(MasterBaseModel):
    class Meta:
        verbose_name = "Furnishing"
        verbose_name_plural = "Furnishings"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Facing(MasterBaseModel):
    class Meta:
        verbose_name = "Facing"
        verbose_name_plural = "Facings"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ConstructionStatus(MasterBaseModel):
    class Meta:
        verbose_name = "Construction Status"
        verbose_name_plural = "Construction Statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OwnershipType(MasterBaseModel):
    class Meta:
        verbose_name = "Ownership Type"
        verbose_name_plural = "Ownership Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ParkingType(MasterBaseModel):
    class Meta:
        verbose_name = "Parking Type"
        verbose_name_plural = "Parking Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Amenity(MasterBaseModel):
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class (e.g. fa-solid fa-dumbbell)",
    )

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        ordering = ["name"]

    def __str__(self):
        return self.name

