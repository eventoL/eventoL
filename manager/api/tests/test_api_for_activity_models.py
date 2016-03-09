import datetime
import unittest
from manager.models import Activity, Comment, TalkProposal, Talk, TalkType, Room, Installation
from manager.api.tests.test_api import api_test


@api_test()
class TestApiActivity():
    fk_models = ['manager.Adress', 'manager.Event']
    str_model = 'manager.Activity'
    model = Activity
    url_base = '/api/activity/'
    example = {
        'title': 'break',
        'long_description': 'break..break..break',
        'confirmed': True,
        'abstract': 'zzzzzzzzzz'
    }


@api_test()
class TestApiComment():
    fk_models = ['auth.User', 'manager.Adress', 'manager.Event', 'manager.Activity']
    str_model = 'manager.Comment'
    model = Comment
    url_base = '/api/comment/'
    example = {
        'created': datetime.datetime.now(),
        'body': 'blablablablable...'
    }


@api_test()
class TestApiTalkProposal():
    fk_models = ['manager.Adress', 'manager.Event', 'manager.Activity', 'manager.TalkType']
    str_model = 'manager.TalkProposal'
    model = TalkProposal
    url_base = '/api/talkproposal/'
    example = {
        'speakers_names': 'pepe,juan,roberto',
        'speakers_email': 'pepe@pepemail.com',
        'labels': 'python,django'
    }


@api_test()
class TestApiTalk():
    fk_models = ['manager.Adress', 'manager.Event', 'manager.Activity', 'manager.TalkType', 'manager.TalkProposal', 'manager.Room']
    str_model = 'manager.Talk'
    model = Talk
    url_base = '/api/talk/'
    example = {
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now()
    }


@api_test()
class TestApiTalkType():
    str_model = 'manager.TalkType'
    model = TalkType
    url_base = '/api/talktype/'
    example = {
        'name': 'conference'
    }


@api_test()
class TestApiRoom():
    fk_models = ['manager.Adress', 'manager.Event', 'manager.TalkType']
    str_model = 'manager.Room'
    model = Room
    url_base = '/api/room/'
    example = {
        'name': 'auditorio'
    }


@api_test()
class TestApiInstallation():
    fk_models = ['manager.HardwareManufacturer', 'manager.Hardware', 'manager.Software', 'auth.User', 'manager.Adress', 'manager.Event', 'manager.EventoLUser', 'manager.InstalationAttendee','manager.Installer']
    str_model = 'manager.Installation'
    model = Installation
    url_base = '/api/installation/'
    example = {
        'notes': 'ok'
    }

if __name__ == '__main__':
    unittest.main()
