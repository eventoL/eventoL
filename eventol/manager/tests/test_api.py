import pytest

from rest_framework.test import RequestsClient, APIRequestFactory


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
