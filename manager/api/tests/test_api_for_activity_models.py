import datetime
import unittest
from activity.models import Activity, Comment, TalkProposal, Talk, TalkType, Room, Installation
from api.tests.test_api import api_test


@api_test()
class TestApiActivity():
    fk_models = ['event.Adress', 'event.Event']
    str_model = 'activity.Activity'
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
    fk_models = ['auth.User', 'event.Adress', 'event.Event', 'activity.Activity']
    str_model = 'activity.Comment'
    model = Comment
    url_base = '/api/comment/'
    example = {
        'created': datetime.datetime.now(),
        'body': 'blablablablable...'
    }


@api_test()
class TestApiTalkProposal():
    fk_models = ['event.Adress', 'event.Event', 'activity.Activity', 'activity.TalkType']
    str_model = 'activity.TalkProposal'
    model = TalkProposal
    url_base = '/api/talkproposal/'
    example = {
        'speakers_names': 'pepe,juan,roberto',
        'speakers_email': 'pepe@pepemail.com',
        'labels': 'python,django'
    }
    # TODO check level: Beginner


@api_test()
class TestApiTalk():
    fk_models = ['event.Adress', 'event.Event', 'activity.Activity', 'activity.TalkType', 'activity.TalkProposal', 'activity.Room']
    str_model = 'activity.Talk'
    model = Talk
    url_base = '/api/talk/'
    example = {
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now()
    }


@api_test()
class TestApiTalkType():
    str_model = 'activity.TalkType'
    model = TalkType
    url_base = '/api/talktype/'
    example = {
        'name': 'conference'
    }


@api_test()
class TestApiRoom():
    fk_models = ['event.Adress', 'event.Event', 'activity.TalkType']
    str_model = 'activity.Room'
    model = Room
    url_base = '/api/room/'
    example = {
        'name': 'auditorio'
    }


@api_test()
class TestApiInstallation():
    fk_models = ['device.HardwareManufacturer', 'device.Hardware', 'device.Software', 'auth.User', 'event.Adress', 'event.Event', 'user.EventoLUser', 'user.InstalationAttendee','user.Installer']
    str_model = 'activity.Installation'
    model = Installation
    url_base = '/api/installation/'
    example = {
        'notes': 'ok'
    }

if __name__ == '__main__':
    unittest.main()
