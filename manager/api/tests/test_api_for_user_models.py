import unittest
from manager.models import Attendee, Collaborator, EventoLUser, InstalationAttendee, Installer, Speaker
from manager.api.tests.test_api import api_test


# User Models
@api_test()
class TestApiAttendee():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event', 'manager.EventoLUser']
    str_model = 'manager.Attendee'
    model = Attendee
    url_base = '/api/attendee/'
    example = {
        'additional_info': 'hola'
    }


@api_test()
class TestApiCollaborator():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event', 'manager.EventoLUser']
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
class TestApiEventoLUser():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event']
    str_model = 'manager.EventoLUser'
    model = EventoLUser
    url_base = '/api/eventoluser/'
    example = {
        'assisted': True
    }


@api_test()
class TestApiInstalationAttendee():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event', 'manager.EventoLUser']
    str_model = 'manager.InstalationAttendee'
    model = InstalationAttendee
    url_base = '/api/instalationattendee/'
    example = {
        'installarion_additional_info': 'hola'
    }


@api_test()
class TestApiSpeaker():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event', 'manager.EventoLUser']
    str_model = 'manager.Speaker'
    model = Speaker
    url_base = '/api/speaker/'
    example = {}


@api_test()
class TestApiInstaller():
    fk_models = ['auth.User', 'manager.Address', 'manager.Event', 'manager.EventoLUser']
    str_model = 'manager.Installer'
    model = Installer
    url_base = '/api/installer/'
    example = {}

if __name__ == '__main__':
    unittest.main()