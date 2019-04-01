# pylint: redefined-outer-name
from datetime import datetime

import autofixture
import pytest

from ..models import generate_ticket_code


@pytest.fixture
@pytest.mark.django_db
def admin():
    yield autofixture.create_one('auth.User', {
        'username': 'testadmin',
        'password': 'secret',
        'is_superuser': True,
        'is_staff': True
    })


# EventTag
@pytest.fixture
@pytest.mark.django_db
def event_tag_1():
    yield autofixture.create_one(
        'manager.EventTag',
        {'name': 'test1', 'slug': 'test1'}
    )


@pytest.fixture
@pytest.mark.django_db
def event_tag_2():
    yield autofixture.create_one(
        'manager.EventTag',
        {'name': 'test2', 'slug': 'test2'}
    )


# Events
@pytest.fixture
@pytest.mark.django_db
def event1(event_tag_1):
    yield autofixture.create_one(
        'manager.Event',
        {'name': 'event1', 'slug': 'event1', 'tags': [event_tag_1]}
    )


@pytest.fixture
@pytest.mark.django_db
def event2(event_tag_2):
    yield autofixture.create_one(
        'manager.Event',
        {'name': 'event2', 'slug': 'event2', 'tags': [event_tag_2]}
    )


# Users
@pytest.fixture
@pytest.mark.django_db
def user1():
    yield autofixture.create_one('auth.User', {
        'username': 'user1',
        'password': 'secret',
        'is_superuser': False,
        'is_staff': False
    })


@pytest.fixture
@pytest.mark.django_db
def user2():
    yield autofixture.create_one('auth.User', {
        'username': 'user2',
        'password': 'secret',
        'is_superuser': False,
        'is_staff': False
    })


# EventUsers
@pytest.fixture
@pytest.mark.django_db
def event_user1(user1, event1):
    yield autofixture.create_one('manager.EventUser', {'user': user1, 'event': event1})


@pytest.fixture
@pytest.mark.django_db
def event_user2(user2, event2):
    yield autofixture.create_one('manager.EventUser', {'user': user2, 'event': event2})


# Attendee without User
@pytest.fixture
@pytest.mark.django_db
def attendee_without_user1(event1):
    yield autofixture.create_one('manager.Attendee', {'event_user': None, 'event': event1})


@pytest.fixture
@pytest.mark.django_db
def attendee_without_user2(event2):
    yield autofixture.create_one('manager.Attendee', {'event_user': None, 'event': event2})


# Attendee From Event User
@pytest.fixture
@pytest.mark.django_db
def attendee_from_event_user1(event_user1, event1):
    yield autofixture.create_one(
        'manager.Attendee', {'event_user': event_user1, 'event': event1, 'email_token': generate_ticket_code()})


@pytest.fixture
@pytest.mark.django_db
def attendee_from_event_user2(event_user2, event2):
    yield autofixture.create_one(
        'manager.Attendee', {'event_user': event_user2, 'event': event2, 'email_token': generate_ticket_code()})


# Organizers
@pytest.fixture
@pytest.mark.django_db
def organizer1(event_user1):
    yield autofixture.create_one('manager.Organizer', {'event_user': event_user1})


@pytest.fixture
@pytest.mark.django_db
def organizer2(event_user2):
    yield autofixture.create_one('manager.Organizer', {'event_user': event_user2})


# Collaborators
@pytest.fixture
@pytest.mark.django_db
def collaborator1(event_user1):
    yield autofixture.create_one('manager.Collaborator', {'event_user': event_user1})


@pytest.fixture
@pytest.mark.django_db
def collaborator2(event_user2):
    yield autofixture.create_one('manager.Collaborator', {'event_user': event_user2})


# Installer
@pytest.fixture
@pytest.mark.django_db
def installer1(event_user1):
    yield autofixture.create_one('manager.Installer', {'event_user': event_user1})


@pytest.fixture
@pytest.mark.django_db
def installer2(event_user2):
    yield autofixture.create_one('manager.Installer', {'event_user': event_user2})


# Reviewer
@pytest.fixture
@pytest.mark.django_db
def reviewer1(event_user1):
    yield autofixture.create_one('manager.Reviewer', {'event_user': event_user1})


@pytest.fixture
@pytest.mark.django_db
def reviewer2(event_user2):
    yield autofixture.create_one('manager.Reviewer', {'event_user': event_user2})


# Activity
@pytest.fixture
@pytest.mark.django_db
def activity1(event1):
    yield autofixture.create_one('manager.Activity', {'event': event1}, generate_fk=True)


@pytest.fixture
@pytest.mark.django_db
def activity2(event2):
    yield autofixture.create_one('manager.Activity', {'event': event2}, generate_fk=True)


# Room
@pytest.fixture
@pytest.mark.django_db
def room1(event1):
    yield autofixture.create_one('manager.Room', {'event': event1})


@pytest.fixture
@pytest.mark.django_db
def room2(event2):
    yield autofixture.create_one('manager.Room', {'event': event2})


# EventDate
@pytest.mark.django_db
def get_event_date(datestring):
    date = datetime.strptime(datestring, "%d/%m/%Y")
    return autofixture.create_one('manager.EventDate', {'date': date.date()})


@pytest.fixture
@pytest.mark.django_db
def event_date_24_01_2019():
    yield get_event_date('24/01/2019')


@pytest.fixture
@pytest.mark.django_db
def event_date_25_01_2019():
    yield get_event_date('25/01/2019')


@pytest.fixture
@pytest.mark.django_db
def event_date_26_01_2019():
    yield get_event_date('26/01/2019')


@pytest.fixture
@pytest.mark.django_db
def event_date_27_01_2019():
    yield get_event_date('27/01/2019')


# Groups
@pytest.fixture
@pytest.mark.django_db
def event_data1(
        event_tag_1, event1, user1,
        event_user1, attendee_without_user1,
        attendee_from_event_user1, organizer1,
        collaborator1, installer1, reviewer1,
        activity1, room1):
    yield {
        'event': event1,
        'event_tag': event_tag_1,
        'user': user1,
        'event_user': event_user1,
        'attendee_without_user': attendee_without_user1,
        'attendee_from_event_user': attendee_from_event_user1,
        'organizer': organizer1,
        'collaborator': collaborator1,
        'installer': installer1,
        'reviewer': reviewer1,
        'activity': activity1,
        'room': room1
    }


@pytest.fixture
@pytest.mark.django_db
def event_data2(
        event_tag_2, event2, user2,
        event_user2, attendee_without_user2,
        attendee_from_event_user2, organizer2,
        collaborator2, installer2, reviewer2,
        activity2, room2):
    yield {
        'event': event2,
        'event_tag': event_tag_2,
        'user': user2,
        'event_user': event_user2,
        'attendee_without_user': attendee_without_user2,
        'attendee_from_event_user': attendee_from_event_user2,
        'organizer': organizer2,
        'collaborator': collaborator2,
        'installer': installer2,
        'reviewer': reviewer2,
        'activity': activity2,
        'room': room2
    }
