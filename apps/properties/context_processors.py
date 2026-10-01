from .models import Project

def project_context(request):
    first_project = Project.objects.filter(is_active=True).order_by("id").first()
    return {
        "first_project": first_project,
    }