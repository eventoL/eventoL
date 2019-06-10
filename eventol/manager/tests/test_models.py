import pytest


@pytest.mark.django_db
def test_event_model(event1):
    assert str(event1) == event1.name
