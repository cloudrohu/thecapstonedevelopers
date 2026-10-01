# my_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Accessing http://127.0.0 triggers the view
    path('about/', views.about, name='about'),
    path('faqs/', views.FAQs, name='faqs'),
    path('privacy-policy/', views.Privacy_Policy, name='privacy_policy'),
    path('disclaimer/', views.Disclaimer, name='disclaimer'),
    path('amenities/', views.Amenities, name='amenities'),
    path('location/', views.Location, name='location'),
    path('gallery/', views.GalleryView, name='gallery'),
    path('contact/', views.ContactView, name='contact'),
    path('thank-you/', views.ThankYouView, name='thank_you'),
    path('developer/', views.Developer, name='developer')    
]
