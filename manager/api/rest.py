from django.contrib.auth.models import User
from rest_framework import routers, serializers
from manager.api.builder import ViewSetBuilder
from manager.forms import CollaboratorRegistrationForm, UserRegistrationForm, TalkProposalForm, \
    AttendeeRegistrationByCollaboratorForm
from manager.models import Collaborator, Sede, TalkProposal, TalkType, ContactType, Contact, Attendee


class SedeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sede
        exclude = ('country', 'state', 'city', 'district', 'place')


SedeViewSet = ViewSetBuilder(Sede, SedeSerializer).build()
UserViewSet = ViewSetBuilder(User, UserRegistrationForm).build()
CollaboratorViewSet = ViewSetBuilder(Collaborator, CollaboratorRegistrationForm).build()
TalkProposalViewSet = ViewSetBuilder(TalkProposal, TalkProposalForm).build()
TalkTypeViewSet = ViewSetBuilder(TalkType).build()
ContactTypeViewSet = ViewSetBuilder(ContactType).build()
ContactViewSet = ViewSetBuilder(Contact).build()
AttendeeViewSet = ViewSetBuilder(Attendee, AttendeeRegistrationByCollaboratorForm).build()


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'sedes', SedeViewSet)
router.register(r'users', UserViewSet)
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'talk_types', TalkTypeViewSet)
router.register(r'talk_proposals', TalkProposalViewSet)
router.register(r'contact_type', ContactTypeViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'attendee', AttendeeViewSet)
