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
router.register(r'talktype', ViewSetBuilder(models.TalkType).build())
router.register(r'talkproposal', ViewSetBuilder(models.TalkProposal, cls_form=forms.TalkProposalForm, reduce_func=reduces.proposals).build())
router.register(r'room', ViewSetBuilder(models.Room).build())
router.register(r'activity', ViewSetBuilder(models.Activity).build())
router.register(r'comment', ViewSetBuilder(models.Comment).build())
router.register(r'installation', ViewSetBuilder(models.Installation, reduce_func=reduces.installations).build())
router.register(r'talk', ViewSetBuilder(models.Talk, reduce_func=reduces.talks).build())

# User Models
router.register(r'installer', ViewSetBuilder(models.Installer, reduce_func=reduces.installers).build())
router.register(r'instalationattendee', ViewSetBuilder(models.InstalationAttendee).build())
router.register(r'attendee', ViewSetBuilder(models.Attendee, cls_form=forms.AttendeeRegistrationByCollaboratorForm, reduce_func=reduces.attendees).build())
router.register(r'collaborator', ViewSetBuilder(models.Collaborator, cls_form=forms.CollaboratorRegistrationForm).build())
router.register(r'eventoluser', ViewSetBuilder(models.EventoLUser).build())
router.register(r'speaker', ViewSetBuilder(models.Speaker).build())

# Event Model
router.register(r'adress', ViewSetBuilder(models.Adress).build())
router.register(r'contact', ViewSetBuilder(models.Contact).build())
router.register(r'contactmessage', ViewSetBuilder(models.ContactMessage).build())
router.register(r'contacttype', ViewSetBuilder(models.ContactType).build())
router.register(r'event', ViewSetBuilder(models.Event).build())
router.register(r'image', ViewSetBuilder(models.Image).build())

# Device Model
router.register(r'hardware', ViewSetBuilder(models.Hardware).build())
router.register(r'hardwaremanufacturer', ViewSetBuilder(models.HardwareManufacturer).build())
router.register(r'software', ViewSetBuilder(models.Software).build())

# Route External
router.register(r'votes', ViewSetBuilder(Vote).build())
router.register(r'content_types', ViewSetBuilder(ContentType).build())