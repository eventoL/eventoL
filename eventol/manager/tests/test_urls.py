from django.urls import reverse, resolve


def test_home_url():
    path = reverse('home')
    assert resolve(path).view_name == 'home'
