from django.test import RequestFactory
from django.urls import reverse

import pytest

from manager import views


@pytest.mark.django_db
def test_home_view(user1):
    path = reverse('home')
    request = RequestFactory().get(path)
    request.user = user1
    request.session = {}

    response = views.home(request)
    assert response.status_code == 200
