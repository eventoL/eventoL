# pylint: redefined-outer-name
import autofixture
import pytest


@pytest.fixture
@pytest.mark.django_db
def admin():
    yield autofixture.create_one('auth.User', {'is_superuser': True, 'is_staff': True})


# Events
@pytest.fixture
@pytest.mark.django_db
def event1():
    yield autofixture.create_one('manager.Event')


@pytest.fixture
@pytest.mark.django_db
def event2():
    yield autofixture.create_one('manager.Event')


# Users
@pytest.fixture
@pytest.mark.django_db
def user1():
    yield autofixture.create_one('auth.User', {'is_superuser': False, 'is_staff': False})


@pytest.fixture
@pytest.mark.django_db
def user2():
    yield autofixture.create_one('auth.User', {'is_superuser': False, 'is_staff': False})


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
