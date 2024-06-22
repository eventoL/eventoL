from django.urls import reverse

import pytest
from pytest_lazyfixture import lazy_fixture
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
    url = request.build_absolute_uri()
    response = api_client.get(url)
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
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.parametrize('api_reverse_name, fields, model', [
    ('event-list', [], lazy_fixture('event1')),
    ('event-list', ['name'], lazy_fixture('event1')),
    ('event-list', ['name', 'abstract', 'event_slug'], lazy_fixture('event1')),
    ('activity-list', [], lazy_fixture('activity1')),
    ('activity-list', ['title'], lazy_fixture('activity1')),
    ('activity-list', ['title', 'abstract', 'start_date'], lazy_fixture('activity1')),
    ('installation-list', [], lazy_fixture('installation1')),
    ('installation-list', ['notes'], lazy_fixture('installation1')),
    ('installation-list', ['software', 'installer'], lazy_fixture('installation1')),
])
@pytest.mark.django_db(transaction=True)
def test_api_filter_fields(api_reverse_name, fields, api_request_factory, api_client, model):
    endpoint = reverse(api_reverse_name)
    fields_string = ','.join(fields)
    url = '{}?fields={}'.format(endpoint, fields_string)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
    if fields:
        assert set(json['results'][0].keys()) == set(fields)


@pytest.mark.django_db(transaction=True)
def test_event_api_my_events(api_request_factory, api_client, event1, event2, organizer1):
    endpoint = reverse('event-list')
    url = '{}?my_events=true'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    api_client.force_authenticate(user=organizer1.event_user.user)
    response = api_client.get(url)

    assert response.status_code == 200

    json = response.json()
    assert len(json['results']) == 1
    assert json['results'][0]['id'] == event1.id

    api_client.logout()


@pytest.mark.django_db(transaction=True)
def test_event_api_tags(api_request_factory, api_client, event1, event2, event_tag_1):
    endpoint = reverse('event-list')
    url = '{}?tags__slug={}'.format(endpoint, event_tag_1.slug)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
    assert len(json['results']) == 1
    assert json['results'][0]['id'] == event1.id


# Test event api ordering
@pytest.mark.django_db(transaction=True)
def test_event_api_ordering_ascending(api_request_factory, api_client, event1, event2):
    endpoint = reverse('event-list')
    url = '{}?ordering=created_at'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 2
    assert json['next'] is None
    assert json['previous'] is None
    assert len(json['results']) == 2
    assert json['results'][0]['id'] == event1.id
    assert json['results'][1]['id'] == event2.id


@pytest.mark.django_db(transaction=True)
def test_event_api_ordering_descending(api_request_factory, api_client, event1, event2):
    endpoint = reverse('event-list')
    url = '{}?ordering=-created_at'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 2
    assert json['next'] is None
    assert json['previous'] is None
    assert len(json['results']) == 2
    assert json['results'][0]['id'] == event2.id
    assert json['results'][1]['id'] == event1.id


@pytest.mark.django_db(transaction=True)
def test_event_api_filter_schedule_confirmed(api_request_factory, api_client, event1, event2):
    event2.schedule_confirmed = True
    event2.save()
    endpoint = reverse('event-list')
    url = '{}?schedule_confirmed=true'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
    assert len(json['results']) == 1
    assert json['results'][0]['id'] == event2.id

    url = '{}?schedule_confirmed=false'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 1
    assert json['next'] is None
    assert json['previous'] is None
    assert len(json['results']) == 1
    assert json['results'][0]['id'] == event1.id


@pytest.mark.django_db(transaction=True)
def test_event_api_pagination(api_request_factory, api_client, event1, event2):
    endpoint = reverse('event-list')
    url = '{}?limit=1&offset=0'.format(endpoint)
    request = api_request_factory.get(url, format='json')
    url = request.build_absolute_uri()
    response = api_client.get(url)
    assert response.status_code == 200

    json = response.json()
    assert json['count'] == 2
    assert json['next'] is not None
    assert json['previous'] is None
    assert len(json['results']) == 1
