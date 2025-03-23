from django.urls import re_path
from django.views.generic.base import TemplateView

from manager import views

event_patterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(
        r"^attendee/confirm/(?P<attendee_id>\d+)/(?P<token>\w+)$",
        views.attendee_confirm_email,
        name="attendee_confirm_email",
    ),
    re_path(r"^FAQ$", views.event_view, name="FAQ", kwargs={"html": "FAQ.html"}),
    re_path(r"^edit$", views.edit_event, name="edit_event"),
    re_path(r"^image-cropping/$", views.event_add_image, name="event_add_image"),
    re_path(r"^draw", views.draw, name="draw"),
    re_path(r"^rooms/list/$", views.rooms_list, name="rooms_list"),
    re_path(r"^rooms/add/$", views.add_or_edit_room, name="add_room"),
    re_path(r"^rooms/edit/(?P<room_id>\d+)/$", views.add_or_edit_room, name="edit_room"),
    re_path(r"^rooms/delete/(?P<room_id>\d+)/$", views.delete_room, name="delete_room"),
    re_path(r"^registration$", views.attendee_registration, name="attendee_registration"),
    re_path(
        r"^registration/attendee/email-sent$",
        TemplateView.as_view(template_name="registration/attendee/email-sent.html"),
        name="attendee_email_sent",
    ),
    re_path(
        r"^registration/attendee/search/(?P<ticket_code>\w+)$",
        views.attendance_by_ticket,
        name="attendance_by_ticket",
    ),
    re_path(r"^registration/attendee/search", views.manage_attendance, name="manage_attendance"),
    re_path(
        r"^registration/attendee/by-collaborator$",
        views.registration_by_collaborator,
        name="attendee_registration_by_collaborator",
    ),
    re_path(
        r"^registration/attendee/from-installation$",
        views.registration_from_installation,
        name="attendee_registration_from_installation",
    ),
    re_path(
        r"^registration/attendee/by-self/(?P<event_registration_code>" r"[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-" r"[89aAbB][a-f0-9]{3}-[a-f0-9]{12})$",
        views.attendee_registration_by_self,
        name="attendee_registration_by_self",
    ),
    re_path(
        r"^registration/attendee/by-self/autoreadqr",
        views.attendance_by_autoreadqr,
        name="attendance_by_autoreadqr",
    ),
    re_path(
        r"^registration/print-code$",
        views.attendee_registration_print_code,
        name="attendee_registration_print_code",
    ),
    re_path(
        r"^registration/collaborator$",
        views.collaborator_registration,
        name="collaborator_registration",
    ),
    re_path(r"^registration/installer$", views.installer_registration, name="installer_registration"),
    re_path(r"^installation$", views.installation, name="installation"),
    re_path(r"^activities$", views.activities, name="activities"),
    re_path(r"^my_proposals$", views.my_proposals, name="my_proposals"),
    re_path(r"^activity/(?P<activity_id>\d+)/$", views.activity_detail, name="activity_detail"),
    re_path(r"^activity/dummy/$", views.activity_dummy, name="activity_dummy"),
    re_path(r"^activity/proposal/$", views.activity_proposal, name="activity_proposal"),
    re_path(
        r"^activity/proposal/(?P<activity_id>\d+)/edit/$",
        views.edit_activity_proposal,
        name="edit_activity_proposal",
    ),
    re_path(
        r"^activity/proposal/image-cropping/(?P<activity_id>\d+)/$",
        views.image_cropping,
        name="image_cropping",
    ),
    re_path(r"^activity/proposal/image-cropping/$", views.image_cropping, name="image_cropping"),
    re_path(
        r"^activity/registration/(?P<proposal_id>\d+)$",
        views.talk_registration,
        name="talk_registration",
    ),
    re_path(r"^activity/confirm_schedule/$", views.confirm_schedule, name="confirm_schedule"),
    re_path(r"^activity/csv/$", views.activities_csv, name="activities_csv"),
    re_path(
        r"^activity/reject_activity/(?P<activity_id>\d+)/$",
        views.reject_activity,
        name="reject_activity",
    ),
    re_path(
        r"^activity/resend_proposal/(?P<activity_id>\d+)/$",
        views.resend_proposal,
        name="resend_proposal",
    ),
    re_path(r"^activity/(?P<activity_id>\d+)/vote/up$", views.activity_vote_up, name="activity_vote_up"),
    re_path(
        r"^activity/(?P<activity_id>\d+)/vote/down$",
        views.activity_vote_down,
        name="activity_vote_down",
    ),
    re_path(
        r"^activity/(?P<activity_id>\d+)/vote/cancel$",
        views.activity_vote_cancel,
        name="activity_vote_cancel",
    ),
    re_path(r"^schedule$", views.schedule, name="schedule"),
    re_path(r"^contact$", views.contact, name="contact"),
    re_path(r"^reports$", views.reports, name="reports"),
    re_path(r"^organizers$", views.add_organizer, name="add_organizer"),
    re_path(r"^registration_people", views.add_registration_people, name="add_registration_people"),
    re_path(r"^reviewers", views.add_reviewer, name="add_reviewer"),
    re_path(r"^ticket$", views.view_ticket, name="view_ticket"),
]
