from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from voting.models import Vote
from rest_framework import serializers

from manager.api import reduces
from manager.api.builder import ViewSetBuilder
from manager import forms
from manager import models
from manager.models import Installer


class SedeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sede
        exclude = ('country', 'state', 'city', 'district', 'place')


class InstallerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Installer
        exclude = ['collaborator']

# Django
UserViewSet = ViewSetBuilder(User, forms.UserRegistrationForm).build()

# EventoL
SedeViewSet = ViewSetBuilder(models.Sede, SedeSerializer).build()
CollaboratorViewSet = ViewSetBuilder(models.Collaborator, forms.CollaboratorRegistrationForm).build()
TalkTypeViewSet = ViewSetBuilder(models.TalkType).build()
TalkProposalViewSet = ViewSetBuilder(models.TalkProposal, forms.TalkProposalForm, reduce_func=reduces.proposals).build()
TalkViewSet = ViewSetBuilder(models.Talk, reduce_func=reduces.talks).build()
ContactTypeViewSet = ViewSetBuilder(models.ContactType).build()
ContactViewSet = ViewSetBuilder(models.Contact).build()
RoomViewSet = ViewSetBuilder(models.Room).build()
InstallationViewSet = ViewSetBuilder(models.Installation, reduce_func=reduces.installations).build()
SoftwareViewSet = ViewSetBuilder(models.Software).build()
HardwareViewSet = ViewSetBuilder(models.Hardware).build()
HardwareManufacturerViewSet = ViewSetBuilder(models.HardwareManufacturer).build()
InstallerViewSet = ViewSetBuilder(models.Installer,
                                  InstallerSerializer,
                                  reduce_func=reduces.installers).build()
AttendeeViewSet = ViewSetBuilder(models.Attendee,
                                 forms.AttendeeRegistrationByCollaboratorForm,
                                 reduce_func=reduces.attendees).build()

# External
VoteViewSet = ViewSetBuilder(Vote).build()
ContentTypeViewSet = ViewSetBuilder(ContentType).build()
