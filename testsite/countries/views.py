from django.http import JsonResponse
from django.db.models import Count, Sum

from countries.models import Region


def stats(request):
    regions = Region.objects.annotate(
        num_countries=Count("countries"), total_population=Sum("countries__population", default=0)
    )
    response = {"regions": []}
    for region in regions:
        region_data = {
            "name": region.name,
            "number_countries": region.num_countries,
            "total_population": region.total_population,
        }
        response["regions"].append(region_data)

    return JsonResponse(response)
