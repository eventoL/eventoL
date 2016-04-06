import unittest
from manager.api.rest import reduces
from manager.models import Attendee, Collaborator, EventUser, InstallationAttendee, Installer, Speaker, \
    NonRegisteredAttendee, Organizer
from manager.tests.api.test_api import api_test


# User Models
@api_test()
class TestApiAttendee():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.Attendee'
    model = Attendee
    url_base = '/api/attendee/'
    example = {
        'additional_info': 'hola'
    }

    def reduce(self, queryset):
        return reduces.attendees(queryset)

@api_test()
class TestApiCollaborator():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.Collaborator'
    model = Collaborator
    url_base = '/api/collaborators/'
    example = {
        'assignation': 'Coffee',
        'time_availability': 'Morning',
        'phone': '123123541',
        'address': 'calle',
        'additional_info': 'hola'
    }


@api_test()
class TestApiEventUser():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee']
    str_model = 'manager.EventUser'
    model = EventUser
    url_base = '/api/eventusers/'
    example = {
        'assisted': True,
        'ticket': True
    }


@api_test()
class TestApiInstallationAttendee():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.InstallationAttendee'
    model = InstallationAttendee
    url_base = '/api/installationattendees/'
    example = {
        'installation_additional_info': 'hola'
    }


@api_test()
class TestApiSpeaker():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.Speaker'
    model = Speaker
    url_base = '/api/speakers/'
    example = {}


@api_test()
class TestApiNonRegisteredAttendee():
    fk_models = []
    str_model = 'manager.NonRegisteredAttendee'
    model = NonRegisteredAttendee
    url_base = '/api/nonregisteredattendees/'
    example = {
        'first_name': 'name',
        'last_name': 'last_name',
        'email': 'email@eamil.com',
        'is_installing': True,
        'installation_additional_info': 'more_info'
    }


@api_test()
class TestApiInstaller():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.Installer'
    model = Installer
    url_base = '/api/installers/'
    example = {}

    def reduce(self, queryset):
        return reduces.installers(queryset)


@api_test()
class TestApiOrganizer():
    fk_models = ['auth.User', 'manager.Event', 'manager.NonRegisteredAttendee', 'manager.EventUser']
    str_model = 'manager.Organizer'
    model = Organizer
    url_base = '/api/organizers/'
    example = {}
