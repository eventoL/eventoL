from manager.api.rest import serializers
from django.contrib.contenttypes.models import ContentType
from voting.models import Vote
from builder import ViewSetBuilder
from rest_framework import routers
from manager import models
from manager import forms
from manager.api.rest import reduces

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Api Model
user_view_set_builder = ViewSetBuilder(models.User, cls_serializer=serializers.UserSerializer)
user_filter_fields = ('username', 'email', 'is_staff')
user_view_set_builder.set_fields(user_filter_fields)
router.register(r'users', user_view_set_builder.build())

# Activity Model
router.register(r'talktypes', ViewSetBuilder(models.TalkType).build())
router.register(r'talkproposals', ViewSetBuilder(models.TalkProposal, cls_form=forms.TalkProposalForm, reduce_func=reduces.proposals).build())
router.register(r'rooms', ViewSetBuilder(models.Room).build())
router.register(r'activities', ViewSetBuilder(models.Activity).build())
router.register(r'comments', ViewSetBuilder(models.Comment).build())
router.register(r'installations', ViewSetBuilder(models.Installation, reduce_func=reduces.installations).build())

# User Models
router.register(r'installers', ViewSetBuilder(models.Installer, reduce_func=reduces.installers).build())
router.register(r'installationattendees', ViewSetBuilder(models.InstallationAttendee).build())
router.register(r'attendee', ViewSetBuilder(models.Attendee, cls_form=forms.AttendeeRegistrationForm, reduce_func=reduces.attendees).build())
router.register(r'collaborators', ViewSetBuilder(models.Collaborator, cls_form=forms.CollaboratorRegistrationForm).build())
router.register(r'eventusers', ViewSetBuilder(models.EventUser).build())
router.register(r'speakers', ViewSetBuilder(models.Speaker).build())
router.register(r'nonregisteredattendees', ViewSetBuilder(models.NonRegisteredAttendee).build())

# Event Model
router.register(r'contacts', ViewSetBuilder(models.Contact).build())
router.register(r'contactmessages', ViewSetBuilder(models.ContactMessage).build())
router.register(r'contacttypes', ViewSetBuilder(models.ContactType).build())
router.register(r'events', ViewSetBuilder(models.Event).build())
router.register(r'images', ViewSetBuilder(models.Image).build())

# Device Model
router.register(r'hardwares', ViewSetBuilder(models.Hardware).build())
router.register(r'softwares', ViewSetBuilder(models.Software).build())

# Route External
router.register(r'votes', ViewSetBuilder(Vote).build())
router.register(r'content_types', ViewSetBuilder(ContentType).build())