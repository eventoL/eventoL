import pytest
from django.urls import resolve
from django.urls import reverse

from .constants import ALL_URLS_DATA


def get_reverse_params(required_params, *args, **kwargs):
    room = kwargs["room"]
    event = kwargs["event"]
    activity = kwargs["activity"]
    event_tag = kwargs["event_tag"]
    event_user = kwargs["event_user"]
    attendee = kwargs["attendee_from_event_user"]
    options = {
        "id": event.id,
        "tag": event_tag.slug,
        "room_id": room.id,
        "activity_id": activity.id,
        "proposal_id": activity.id,
        "attendee_id": attendee.id,
        "token": attendee.email_token,
        "event_slug": event.event_slug,
        "ticket_code": event_user.ticket.code,
        "event_registration_code": event.registration_code,
    }
    params = {}
    for param in required_params:
        params[param] = options[param]
    return params


def full_view_name(response):
    module_name = response.func.__module__
    function_name = response.func.__name__
    if hasattr(response.func, "view_class"):
        module_name = response.func.view_class.__module__
        function_name = response.func.view_class.__name__
    return f"{module_name}.{function_name}"


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("url_name, view_name, required_params", ALL_URLS_DATA)
def test_relationship_url_name_with_view_name(url_name, view_name, required_params, event_data1):
    params = get_reverse_params(required_params, **event_data1)
    path = reverse(url_name, kwargs=params)
    response = resolve(path)
    assert full_view_name(response) == view_name
