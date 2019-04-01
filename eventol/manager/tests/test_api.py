from django.test import Client
from django.core.urlresolvers import reverse
from rest_framework.test import RequestsClient, APIRequestFactory

import pytest

from .constants import ALL_API_URL_NAMES


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url_name', ALL_API_URL_NAMES)
def test_anonymous_user_should_see_all_api_endpoints(url_name):
    client = Client()
    endpoint = reverse(url_name)
    response = client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_event():
    factory = APIRequestFactory()
    client = RequestsClient()
    request = factory.get('/api/events/', format='json')
    url = request.get_raw_uri()
    response = client.get(url)
    assert response.ok
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 0
    assert json['next'] is None
    assert json['previous'] is None
    assert json['results'] == []
