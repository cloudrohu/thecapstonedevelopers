from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

   

    path(
        "grappelli/",
        include("grappelli.urls"),
    ),

    

    path(
        "admin/",
        admin.site.urls,
    ),

    

    path(
        "admin/ajax/",
        include("apps.utility.admin.urls"),
    ),

    
    path(
        "",
        include("apps.core.urls"),
    ),

    

    path(
        "",
        include("apps.dashboard.urls"),
    ),


    path(
        "jobs/",
        include("apps.job.urls"),
    ),


   

    path(
        "companies/",
        include("apps.companies.urls"),
    ),

    path("projects/",include("apps.properties.urls"),),

    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls"),
    ),

    

    path(
        "importer/",
        include("apps.importer.urls"),
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )