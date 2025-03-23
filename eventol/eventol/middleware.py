from django.utils.cache import patch_vary_headers
from manager.models import Event


class SubdomainMiddleware:
    @staticmethod
    def process_request(request):
        fqdn = request.get_host().split(":")[0]
        try:
            event = Event.objects.get(cname=fqdn)
        except Event.DoesNotExist:
            pass
        else:
            event_url = event.get_absolute_url()
            if event_url in request.path:
                request.path = request.path.replace(event_url[:-1], "")
            if request.path == "/":
                request.path_info = event.get_absolute_url()[:-1] + request.path

    @staticmethod
    def process_response(_, response):
        patch_vary_headers(response, ("Host",))
        return response
