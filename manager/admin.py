from django.contrib.gis import admin
from manager.models import (Building, Sede, Attendee, Collaborator,
                            HardwareManufacturer, Hardware, Software,
                            Installer, Installation, TalkProposal, Talk,
                            TalkType, Room, TalkTime, ContactType, Contact)
from image_cropping.admin import ImageCroppingMixin


class TalkProposalAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class SedeAdmin(admin.ModelAdmin):
    raw_id_fields = ('city', 'district',)


admin.site.register(Building)
admin.site.register(Sede, SedeAdmin)
admin.site.register(Attendee)
admin.site.register(Collaborator)
admin.site.register(HardwareManufacturer)
admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Installer)
admin.site.register(Installation)
admin.site.register(TalkType)
admin.site.register(TalkProposal, TalkProposalAdmin)
admin.site.register(Room)
admin.site.register(TalkTime)
admin.site.register(Talk)
admin.site.register(ContactType)
admin.site.register(Contact)
