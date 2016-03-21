import unittest
from manager.models import Attendee, Collaborator, EventUser, InstallationAttendee, Installer, Speaker
from manager.api.tests.test_api import api_test


# User Models
@api_test()
class TestApiAttendee():
    fk_models = ['auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.Attendee'
    model = Attendee
    url_base = '/api/attendee/'
    example = {
        'additional_info': 'hola'
    }


@api_test()
class TestApiCollaborator():
    fk_models = ['auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.Collaborator'
    model = Collaborator
    url_base = '/api/collaborator/'
    example = {
        'assignation': 'Coffee',
        'time_availability': 'Morning',
        'phone': '123123541',
        'address': 'calle',
        'additional_info': 'hola'
    }


@api_test()
class TestApiEventUser():
    fk_models = ['auth.User', 'manager.Event']
    str_model = 'manager.EventUser'
    model = EventUser
    url_base = '/api/eventuser/'
    example = {
        'assisted': True
    }


@api_test()
class TestApiInstallationAttendee():
    fk_models = ['auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.InstallationAttendee'
    model = InstallationAttendee
    url_base = '/api/installationattendee/'
    example = {
        'installation_additional_info': 'hola'
    }


@api_test()
class TestApiSpeaker():
    fk_models = ['auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.Speaker'
    model = Speaker
    url_base = '/api/speaker/'
    example = {}


@api_test()
class TestApiInstaller():
    fk_models = ['auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.Installer'
    model = Installer
    url_base = '/api/installer/'
    example = {}

if __name__ == '__main__':
    unittest.main()