from django.contrib.gis import admin
from manager.models import (Building, Sede, Attendee, Collaborator,
                            HardwareManufacturer, Hardware, Software,
                            Installer, Installation, TalkProposal, Talk,
                            TalkType, Room, ContactType, Contact, Comment)
from image_cropping.admin import ImageCroppingMixin


class EventoLAdmin(admin.ModelAdmin):

    def filter_sede(self, sede, queryset):
        return queryset.filter(sede=sede)

    def queryset(self, request):
        queryset = super(EventoLAdmin, self).queryset(request)
        if request.user.is_superuser:
            return queryset
        collaborator = Collaborator.objects.get(user=request.user)
        return self.filter_sede(collaborator.sede, queryset)


class TalkProposalAdmin(ImageCroppingMixin, EventoLAdmin):
    pass


class SedeAdmin(EventoLAdmin):
    raw_id_fields = ('city', 'district',)

    def filter_sede(self, sede, queryset):
        return queryset.filter(name=sede.name)


class CommentAdmin(EventoLAdmin):
    display_fields = ["proposal", "title", "created", "user"]

    def filter_sede(self, sede, queryset):
        return queryset.filter(proposal__sede=sede)


class BuildingAdmin(EventoLAdmin):

    def filter_sede(self, sede, queryset):
        return queryset.filter(address=sede.place.address)


class InstallerAdmin(EventoLAdmin):

    def filter_sede(self, sede, queryset):
        return queryset.filter(collaborator__sede=sede)


class InstallationAdmin(EventoLAdmin):

    def filter_sede(self, sede, queryset):
        return queryset.filter(installer__collaborator__sede=sede)


class TalkAdmin(EventoLAdmin):

    def filter_sede(self, sede, queryset):
        return queryset.filter(talk_proposal__sede=sede)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Sede, SedeAdmin)
admin.site.register(TalkProposal, TalkProposalAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Attendee, EventoLAdmin)
admin.site.register(Collaborator, EventoLAdmin)
admin.site.register(HardwareManufacturer)
admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Installer, InstallerAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(TalkType)
admin.site.register(Room, EventoLAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(ContactType)
admin.site.register(Contact, EventoLAdmin)
