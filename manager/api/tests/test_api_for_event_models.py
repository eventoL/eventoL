import unittest
import datetime
from api.tests.test_api import api_test
from event.models import Adress, Contact, ContactMessage, ContactType, Event, Image


# Event Models
@api_test()
class TestApiAdress():
    str_model = 'event.Adress'
    model = Adress
    url_base = '/api/adress/'
    example = {
        'name': 'home',
        'adress': 'adressssss',
        'latitude': 57.34,
        'longitude': 120.65
    }


@api_test()
class TestApiContact():
    fk_models = ['event.Adress', 'event.Event', 'event.ContactType']
    str_model = 'event.Contact'
    model = Contact
    url_base = '/api/contact/'
    example = {
        'url': 'http://event..com',
        'text': 'text'
    }


@api_test()
class TestApiContactMessage():
    str_model = 'event.ContactMessage'
    model = ContactMessage
    url_base = '/api/contactmessage/'
    example = {
        'name': 'Pepe',
        'email': 'pepe@mail.com',
        'message': 'text_message'
    }


@api_test()
class TestApiContactType():
    str_model = 'event.ContactType'
    model = ContactType
    url_base = '/api/contacttype/'
    example = {
        'name': 'Facebook',
        'icon_class': 'facebook-ico'
    }


@api_test()
class TestApiEvent():
    fk_models = ['event.Adress']
    str_model = 'event.Event'
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
    fk_models = ['event.Adress', 'event.Event']
    str_model = 'event.Image'
    model = Image
    url_base = '/api/image/'
    example = {
        'type': 'png',
        'url': 'http://image/id',
        'cropping': '1024x1234',
    }

if __name__ == '__main__':
    unittest.main()
