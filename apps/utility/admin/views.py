from django.http import JsonResponse
from apps.utility.models import Location


def get_localities(request):

    city_id = request.GET.get("city")

    if not city_id:
        return JsonResponse([], safe=False)

    try:
        city = Location.objects.get(pk=city_id)
    except Location.DoesNotExist:
        return JsonResponse([], safe=False)

    rows = city.get_children().filter(
        is_active=True,
    ).order_by("name")

    return JsonResponse(
        [
            {
                "id": row.pk,
                "name": row.name,
            }
            for row in rows
        ],
        safe=False,
    )


def get_areas(request):

    locality_id = request.GET.get("locality")

    if not locality_id:
        return JsonResponse([], safe=False)

    try:
        locality = Location.objects.get(pk=locality_id)
    except Location.DoesNotExist:
        return JsonResponse([], safe=False)

    rows = locality.get_children().filter(
        is_active=True,
    ).order_by("name")

    return JsonResponse(
        [
            {
                "id": row.pk,
                "name": row.name,
            }
            for row in rows
        ],
        safe=False,
    )