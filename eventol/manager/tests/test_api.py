from django.core.urlresolvers import reverse

import pytest

from eventol.api import EventSerializer
from .constants import ALL_API_URL_NAMES, ALL_API_URLS_REQUIRED_FROM_PAGE


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url_name', ALL_API_URL_NAMES)
def test_anonymous_user_should_see_all_api_endpoints(url_name, web_client):
    endpoint = reverse(url_name)
    response = web_client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_event(api_request_factory, api_client, event1):
    request = api_request_factory.get('/api/events/', format='json')
    url = request.get_raw_uri()
    response = api_client.get(url)
    assert response.ok
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
    assert json['results'][0]['name'] == EventSerializer(event1, context={'request': request}).data['name']


@pytest.mark.parametrize('api_reverse_name, query_params', ALL_API_URLS_REQUIRED_FROM_PAGE)
@pytest.mark.django_db(transaction=True)
def test_index_query(api_reverse_name, query_params, api_request_factory, api_client, event_data1):
    endpoint = reverse(api_reverse_name)
    url = '{}?{}'.format(endpoint, query_params)
    request = api_request_factory.get(url, format='json')
    url = request.get_raw_uri()
    response = api_client.get(url)
    assert response.ok
    assert response.status_code == 200

@pytest.mark.parametrize('api_reverse_name, fields, model', [
    ('event-list', [], pytest.lazy_fixture('event1')),
    ('event-list', ['name'], pytest.lazy_fixture('event1')),
    ('event-list', ['name', 'abstract', 'event_slug'], pytest.lazy_fixture('event1')),
    ('activity-list', [], pytest.lazy_fixture('activity1')),
    ('activity-list', ['title'], pytest.lazy_fixture('activity1')),
    ('activity-list', ['title', 'abstract', 'start_date'], pytest.lazy_fixture('activity1')),
    ('installation-list', [], pytest.lazy_fixture('installation1')),
    ('installation-list', ['notes'], pytest.lazy_fixture('installation1')),
    ('installation-list', ['software', 'installer'], pytest.lazy_fixture('installation1')),
])
@pytest.mark.django_db(transaction=True)
def test_api_filter_fields(api_reverse_name, fields, api_request_factory, api_client, model):
    endpoint = reverse(api_reverse_name)
    fields_string = ','.join(fields)
    url = '{}?fields={}'.format(endpoint, fields_string)
    request = api_request_factory.get(url, format='json')
    url = request.get_raw_uri()
    response = api_client.get(url)
    assert response.ok
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
