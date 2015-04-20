from django.http import HttpResponse
import json

from manager.models import Sede, Talk


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
    response_data[''] = '----------------'
    for place in places:
        response_data[place.id] = place.name
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def sedes_geo(request):
    response_data = [sede.get_geo_info() for sede in Sede.objects.distinct()]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def talks(request, sede_url):
    scheduled_talks = Talk.objects.filter(talk_proposal__sede__url__iexact=sede_url,
                                          talk_proposal__confirmed=True,
                                          talk_proposal__dummy_talk=False
                                          )

    response_data = [talk.get_schedule_info() for talk in scheduled_talks]
    return HttpResponse(json.dumps(response_data), content_type="application/json")