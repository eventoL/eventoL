from rest_framework import routers
from view_sets import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Django
router.register(r'users', UserViewSet)

# EventoL
router.register(r'sedes', SedeViewSet)
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'talks', TalkViewSet)
router.register(r'talk_types', TalkTypeViewSet)
router.register(r'talk_proposals', TalkProposalViewSet)
router.register(r'contact_type', ContactTypeViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'attendee', AttendeeViewSet)
router.register(r'installations', InstallationViewSet)
router.register(r'softwares', SoftwareViewSet)
router.register(r'hardwares', HardwareViewSet)
router.register(r'hardware_manufacturers', HardwareManufacturerViewSet)
router.register(r'installers', InstallerViewSet)

# Route External
router.register(r'votes', VoteViewSet)
router.register(r'content_types', ContentTypeViewSet)
