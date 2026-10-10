import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, expectedCode',
    [
        ('/', 200),
        ('/api/', 200),
        ('/accounts/login/', 200),
        # ('/admin/', 200), # 302 to admin login
        # ('/create-event/', 200), # 302 to account login
        ('/report', 200),
    ],
)
def test_get_page_with_anonymous_user(url, expected_code, web_client):
    response = web_client.get(url)
    assert response.status_code == expected_code
