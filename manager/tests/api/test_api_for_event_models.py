import unittest
import datetime
from manager.tests.api.test_api import api_test
from manager.models import Contact, ContactMessage, ContactType, Event, Image


# Event Models
@api_test()
class TestApiContact():
    fk_models = ['manager.Event', 'manager.ContactType']
    str_model = 'manager.Contact'
    model = Contact
    url_base = '/api/contacts/'
    example = {
        'url': 'http://manager..com',
        'text': 'text'
    }


@api_test()
class TestApiContactMessage():
    str_model = 'manager.ContactMessage'
    model = ContactMessage
    url_base = '/api/contactmessages/'
    example = {
        'name': 'Pepe',
        'email': 'pepe@mail.com',
        'message': 'text_message'
    }


@api_test()
class TestApiContactType():
    str_model = 'manager.ContactType'
    model = ContactType
    url_base = '/api/contacttypes/'
    example = {
        'name': 'Facebook',
        'icon_class': 'facebook-ico'
    }


@api_test()
class TestApiEvent():
    fk_models = ['manager.Image']
    str_model = 'manager.Event'
    model = Event
    url_base = '/api/events/'
    example = {
        'name': 'event',
        'slug': 'event1',
        'external_url': 'http://event1.io',
        'email': 'event@mail.com',
        'event_information': 'best_event',
        'date': datetime.date.today(),
        'limit_proposal_date': datetime.date.today(),
        'schedule_confirm': False,
        'place': "{\"lala\":\"lele\"}"
    }


@api_test()
class TestApiImage():
    fk_models = ['manager.Event']
    str_model = 'manager.Image'
    model = Image
    url_base = '/api/images/'
    example = {}
