from django.contrib import admin

from manager import models
from manager.admin import admins

admin.site.register(models.Activity, admins.ActivityAdmin)
admin.site.register(models.ActivityType, admins.ActivityTypeAdmin)
admin.site.register(models.Attendee, admins.AttendeeAdmin)
admin.site.register(models.AttendeeAttendanceDate, admins.AttendeeAttendanceDateAdmin)
admin.site.register(models.Collaborator, admins.CollaboratorAdmin)
admin.site.register(models.Contact, admins.ContactAdmin)
admin.site.register(models.ContactMessage, admins.ContactMessageAdmin)
admin.site.register(models.ContactType, admins.ContactTypeAdmin)
admin.site.register(models.Event, admins.EventAdmin)
admin.site.register(models.EventDate, admins.EventDateAdmin)
admin.site.register(models.EventolSetting, admins.EventolSettingAdmin)
admin.site.register(models.EventTag, admins.EventTagAdmin)
admin.site.register(models.EventUser, admins.EventUserAdmin)
admin.site.register(models.EventUserAttendanceDate, admins.EventUserAttendanceDateAdmin)
admin.site.register(models.Hardware, admins.HardwareAdmin)
admin.site.register(models.Installation, admins.InstallationAdmin)
admin.site.register(models.InstallationMessage, admins.InstallationMessageAdmin)
admin.site.register(models.Installer, admins.InstallerAdmin)
admin.site.register(models.Organizer, admins.OrganizerAdmin)
admin.site.register(models.Reviewer, admins.ReviewerAdmin)
admin.site.register(models.Room, admins.RoomAdmin)
admin.site.register(models.Software, admins.SoftwareAdmin)
admin.site.register(models.Ticket, admins.TicketAdmin)
