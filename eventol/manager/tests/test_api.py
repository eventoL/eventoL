from django.core.urlresolvers import reverse

import pytest

from .constants import ALL_API_URL_NAMES


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url_name', ALL_API_URL_NAMES)
def test_anonymous_user_should_see_all_api_endpoints(url_name, web_client):
    endpoint = reverse(url_name)
    response = web_client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_event(api_request_factory, api_client):
    request = api_request_factory.get('/api/events/', format='json')
    url = request.get_raw_uri()
    response = api_client.get(url)
    assert response.ok
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 0
    assert json['next'] is None
    assert json['previous'] is None
    assert json['results'] == []
