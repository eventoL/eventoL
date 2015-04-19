from django.contrib.gis import admin
from image_cropping.admin import ImageCroppingMixin
from import_export import resources
from import_export.admin import ExportMixin

from manager.models import (Building, Sede, Attendee, Collaborator,
                            HardwareManufacturer, Hardware, Software,
                            Installer, Installation, TalkProposal, Talk,
                            TalkType, Room, ContactType, Contact, Comment)


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
    display_fields = ["proposal", "created", "user"]

    def filter_sede(self, sede, queryset):
        return queryset.filter(proposal__sede=sede)


class BuildingAdmin(EventoLAdmin):
    def filter_sede(self, sede, queryset):
        return queryset.filter(address=sede.place.address)


class InstallerAdmin(EventoLAdmin):
    def filter_sede(self, sede, queryset):
        return queryset.filter(collaborator__sede=sede)


class InstallationResource(resources.ModelResource):
    class Meta:
        model = Installation
        fields = (
            'hardware__type', 'hardware__manufacturer__name', 'hardware__model', 'hardware__serial', 'software__type',
            'software__name', 'software__version', 'attendee__email', 'installer__collaborator__user__username',
            'notes')
        export_order = fields


class InstallationAdmin(ExportMixin, EventoLAdmin):
    resource_class = InstallationResource
    
    def filter_sede(self, sede, queryset):
        return queryset.filter(installer__collaborator__sede=sede)


class TalkAdmin(EventoLAdmin):
    def filter_sede(self, sede, queryset):
        return queryset.filter(talk_proposal__sede=sede)


class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = ('name', 'surname', 'nickname', 'email', 'assisted', 'is_going_to_install', 'additional_info')
        export_order = fields


class AttendeeAdmin(ExportMixin, EventoLAdmin):
    resource_class = AttendeeResource
    pass


class CollaboratorResource(resources.ModelResource):
    class Meta:
        model = Collaborator
        fields = (
            'user__first_name', 'user__last_name', 'user__username', 'user__email', 'user__date_joined', 'phone',
            'address',
            'assisted', 'assignation', 'time_availability', 'additional_info')

        export_order = fields


class CollaboratorAdmin(ExportMixin, EventoLAdmin):
    resource_class = CollaboratorResource
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(Sede, SedeAdmin)
admin.site.register(TalkProposal, TalkProposalAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
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
