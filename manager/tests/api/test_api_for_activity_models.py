import datetime
import unittest
from manager.models import Activity, Comment, TalkProposal, TalkType, Room, Installation
from manager.tests.api.test_api import api_test
from manager.api.rest import reduces


@api_test()
class TestApiActivity():
    fk_models = ['manager.Event']
    str_model = 'manager.Activity'
    model = Activity
    url_base = '/api/activities/'
    example = {
        'title': 'break',
        'long_description': 'break..break..break',
        'confirmed': True,
        'abstract': 'zzzzzzzzzz',
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now()
    }


@api_test()
class TestApiComment():
    fk_models = ['auth.User', 'manager.NonRegisteredAttendee', 'manager.Event', 'manager.EventUser', 'manager.Room', 'manager.Activity']
    str_model = 'manager.Comment'
    model = Comment
    url_base = '/api/comments/'
    example = {
        'body': 'blablablablable...'
    }


@api_test()
class TestApiTalkProposal():
    fk_models = ['manager.Event', 'manager.Activity', 'manager.TalkType', 'manager.Image']
    str_model = 'manager.TalkProposal'
    model = TalkProposal
    url_base = '/api/talkproposals/'
    example = {
        'speakers_names': 'pepe,juan,roberto',
        'speakers_email': 'pepe@pepemail.com',
        'labels': 'python,django'
    }

    def reduce(self, queryset):
        return reduces.proposals(queryset)


@api_test()
class TestApiTalkType():
    str_model = 'manager.TalkType'
    model = TalkType
    url_base = '/api/talktypes/'
    example = {
        'name': 'conference'
    }


@api_test()
class TestApiRoom():
    fk_models = ['manager.Event']
    str_model = 'manager.Room'
    model = Room
    url_base = '/api/rooms/'
    example = {
        'name': 'auditorio'
    }


@api_test()
class TestApiInstallation():
    fk_models = ['manager.Hardware', 'manager.Software', 'auth.User', 'manager.Event', 'manager.EventUser']
    str_model = 'manager.Installation'
    model = Installation
    url_base = '/api/installations/'
    example = {
        'notes': 'ok'
    }

    def reduce(self, queryset):
        return reduces.installations(queryset)


if __name__ == '__main__':
    unittest.main()
