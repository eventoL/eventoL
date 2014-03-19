from django.http import HttpResponse
import json

from manager.models import Sede


def states(request):
    country = request.GET.get('country', '')
    sedes = Sede.objects.filter(country__code=country).prefetch_related('state')
    regions = [sede.state for sede in sedes]
    response_data = {}
    for region in regions:
        response_data[region.code] = region.name_std
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def cities(request):
    region = request.GET.get('state', '')
    sedes = Sede.objects.filter(state__code=region).prefetch_related('city')
    citiess = [sede.city for sede in sedes]
    response_data = {}
    for city in citiess:
        response_data[city.name_std] = city.name_std
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def sedes(request):
    city = request.GET.get('city', '')
    places = Sede.objects.filter(city__name_std=city)
    response_data = {}
    for place in places:
        response_data[place.id] = place.name
    return HttpResponse(json.dumps(response_data), content_type="application/json")