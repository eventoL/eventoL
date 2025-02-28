import pytest

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.db import connection

from manager.models import Software
from manager.forms import SoftwareAutocomplete
from manager.utils.forms import USE_POSTGRES


def create_autocomplete_form(formclass, query, user):
    autocomplete_form = formclass()
    autocomplete_form.request = RequestFactory()
    autocomplete_form.request.user = user
    autocomplete_form.q = query
    return autocomplete_form


@pytest.mark.django_db
def test_software_autocomplete_form_with_anonymous_user(softwares):
    software_autocomplete_form = create_autocomplete_form(
        SoftwareAutocomplete, 'soft', AnonymousUser())
    assert list(software_autocomplete_form.get_queryset()) == list(Software.objects.none())

@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_without_softwares(user1):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'soft', user1)
    assert list(software_autocomplete_form.get_queryset()) == []

@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_softwares(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'soft', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1, software2]


@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_and_filter_softwares(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'software1', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1]


@pytest.mark.django_db
@pytest.mark.skipif(not USE_POSTGRES, reason="Test only applicable for PostgreSQL")
def test_software_autocomplete_form_with_authenticated_user_get_softwares_with_unaccent(user1, software1, software2):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, 'SóFtwÅrÉ', user1)
    assert list(software_autocomplete_form.get_queryset()) == [software1, software2]

@pytest.mark.django_db
def test_software_autocomplete_form_with_authenticated_user_get_only_5_softwares(user1, softwares):
    software_autocomplete_form = create_autocomplete_form(SoftwareAutocomplete, '', user1)
    softwares_list = list(software_autocomplete_form.get_queryset())
    assert len(softwares_list) < len(softwares)
    assert len(softwares_list) == 5
