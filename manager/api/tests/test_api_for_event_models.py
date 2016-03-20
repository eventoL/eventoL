import unittest
import datetime
from manager.api.tests.test_api import api_test
from manager.models import Contact, ContactMessage, ContactType, Event, Image


# Event Models
@api_test()
class TestApiContact():
    fk_models = ['manager.Event', 'manager.ContactType']
    str_model = 'manager.Contact'
    model = Contact
    url_base = '/api/contact/'
    example = {
        'url': 'http://manager..com',
        'text': 'text'
    }


@api_test()
class TestApiContactMessage():
    str_model = 'manager.ContactMessage'
    model = ContactMessage
    url_base = '/api/contactmessage/'
    example = {
        'name': 'Pepe',
        'email': 'pepe@mail.com',
        'message': 'text_message'
    }


@api_test()
class TestApiContactType():
    str_model = 'manager.ContactType'
    model = ContactType
    url_base = '/api/contacttype/'
    example = {
        'name': 'Facebook',
        'icon_class': 'facebook-ico'
    }


@api_test()
class TestApiEvent():
    fk_models = []
    str_model = 'manager.Event'
    model = Event
    url_base = '/api/event/'
    example = {
        'name': 'event',
        'url': 'event1',
        'external_url': 'http://event1.io',
        'email': 'event@mail.com',
        'event_information': 'best_event',
        'date': datetime.date.today(),
        'limit_proposal_date': datetime.date.today(),
        'schedule_confirm': False
    }


@api_test()
class TestApiImage():
    fk_models = ['manager.Event']
    str_model = 'manager.Image'
    model = Image
    url_base = '/api/image/'
    example = {
        'type': 'png',
        'url': 'http://image/id',
        'cropping': '1024x1234',
    }

if __name__ == '__main__':
    unittest.main()
