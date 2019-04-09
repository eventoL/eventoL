# TESTING
ADMIN_USERNAME = 'testadmin'
ADMIN_PASSWORD = 'secret'

USER_USERNAME_1 = 'user1'
USER_USERNAME_2 = 'user2'
USER_PASSWORD_1 = 'secret'
USER_PASSWORD_2 = 'secret'

EVENT_TAG_NAME_1 = 'test1'
EVENT_TAG_NAME_2 = 'test2'
EVENT_TAG_SLUG_1 = 'test1'
EVENT_TAG_SLUG_2 = 'test2'

EVENT_NAME_1 = 'event1'
EVENT_NAME_2 = 'event2'
EVENT_SLUG_1 = 'event1'
EVENT_SLUG_2 = 'event2'

# URLS AND VIEWS

# Admin
ADMIN_MODELS = [
    'contact', 'contactmessage', 'eventtag',
    'activity', 'room', 'installationmessage',
    'eventuserattendancedate', 'software',
    'eventuser', 'customform', 'attendeeattendancedate',
    'organizer', 'contacttype', 'installer',
    'activitytype', 'hardware', 'collaborator', 'attendee',
    'event', 'installation', 'ticket', 'eventolsetting'
]

ADMIN_URL_NAMES = [
    'admin:manager_{0}_changelist',
    'admin:manager_{0}_change',
    'admin:manager_{0}_delete',
    'admin:manager_{0}_history',
    'admin:manager_{0}_add',
    'admin:manager_{0}_export'
]

ADMIN_DEFAULT_URL_NAMES = [
    'admin:index',
    'admin:jsi18n',
    'admin:login',
    'admin:logout',
    'admin:password_change',
    'admin:auth_user_changelist',
    'admin:auth_group_changelist'
]

ADMIN_URL_NAMES_FOR_APPS = [
    'admin:account_emailaddress_changelist',
    'admin:forms_form_changelist',
    'admin:sites_site_changelist',
    'admin:socialaccount_socialaccount_changelistd'
]

ALL_ADMIN_MODELS_URLS_NAMES = [
    url_name.format(model)
    for model in ADMIN_MODELS
    for url_name in ADMIN_URL_NAMES
]

ALL_ADMIN_URLS_NAMES = ADMIN_DEFAULT_URL_NAMES + \
    ALL_ADMIN_MODELS_URLS_NAMES + \
    ADMIN_URL_NAMES_FOR_APPS

# autocomplete
AUTOCOMPLETE_URLS_DATA = [
    ('all-attendee-autocomplete', 'manager.forms.AllAttendeeAutocomplete', []),
    ('attendee-autocomplete', 'manager.forms.AttendeeAutocomplete', []),
    ('eventuser-autocomplete', 'manager.forms.EventUserAutocomplete', []),
    ('software-autocomplete', 'manager.forms.SoftwareAutocomplete', [])
]
AUTOCOMPLETE_URL_NAMES = [data[0] for data in AUTOCOMPLETE_URLS_DATA]

# Accounts
ACCOUNTS_URL_NAMES = [
    'account_login',
    'account_logout',
    'user_profile',
    'account_signup'
]

# Api
API_BASE_URL_NAME = 'api-root'
API_MODELS = [
    'activity', 'attendee', 'collaborator', 'eventuser',
    'event', 'hardware', 'installation', 'installer',
    'organizer', 'room', 'software', 'eventtag'
]
API_URL_NAMES = ['{0}-list'.format(model) for model in API_MODELS]
ALL_API_URL_NAMES = [API_BASE_URL_NAME] + API_URL_NAMES

# Event
EVENT_URLS_DATA = [
    ('home', 'manager.views.home', []),
    ('create_event', 'manager.views.create_event', []),
    ('index', 'manager.views.index', ['event_slug']),
    ('tag_index', 'manager.views.event_tag_index', ['tag']),
    ('generic_report', 'manager.views.generic_report', []),
    ('FAQ', 'manager.views.event_view', ['event_slug']),
    ('activities', 'manager.views.activities', ['event_slug']),
    ('activity_detail', 'manager.views.activity_detail', ['event_slug', 'activity_id']),
    ('activity_vote_cancel', 'manager.views.activity_vote_cancel', ['event_slug', 'activity_id']),
    ('activity_vote_down', 'manager.views.activity_vote_down', ['event_slug', 'activity_id']),
    ('activity_vote_up', 'manager.views.activity_vote_up', ['event_slug', 'activity_id']),
    ('confirm_schedule', 'manager.views.confirm_schedule', ['event_slug']),
    ('activity_proposal', 'manager.views.activity_proposal', ['event_slug']),
    ('edit_activity_proposal', 'manager.views.edit_activity_proposal', ['event_slug', 'activity_id']),
    ('image_cropping', 'manager.views.image_cropping', ['event_slug']),
    ('image_cropping', 'manager.views.image_cropping', ['event_slug', 'activity_id']),
    ('talk_registration', 'manager.views.talk_registration', ['event_slug', 'proposal_id']),
    ('reject_activity', 'manager.views.reject_activity', ['event_slug', 'activity_id']),
    ('resend_proposal', 'manager.views.resend_proposal', ['event_slug', 'activity_id']),
    ('attendee_confirm_email', 'manager.views.attendee_confirm_email', ['event_slug', 'attendee_id', 'token']),
    ('contact', 'manager.views.contact', ['event_slug']),
    ('draw', 'manager.views.draw', ['event_slug']),
    ('edit_event', 'manager.views.edit_event', ['event_slug']),
    ('event_add_image', 'manager.views.event_add_image', ['event_slug']),
    ('installation', 'manager.views.installation', ['event_slug']),
    ('my_proposals', 'manager.views.my_proposals', ['event_slug']),
    ('add_organizer', 'manager.views.add_organizer', ['event_slug']),
    ('attendee_registration', 'manager.views.attendee_registration', ['event_slug']),
    ('attendee_registration_by_collaborator', 'manager.views.registration_by_collaborator', ['event_slug']),
    ('attendee_registration_by_self', 'manager.views.attendee_registration_by_self', ['event_slug', 'event_registration_code']),
    ('attendance_by_autoreadqr', 'manager.views.attendance_by_autoreadqr', ['event_slug']),
    ('attendee_email_sent', 'django.views.generic.base.TemplateView', ['event_slug']),
    ('attendee_registration_from_installation', 'manager.views.registration_from_installation', ['event_slug']),
    ('manage_attendance', 'manager.views.manage_attendance', ['event_slug']),
    ('attendance_by_ticket', 'manager.views.attendance_by_ticket', ['event_slug', 'ticket_code']),
    ('collaborator_registration', 'manager.views.collaborator_registration', ['event_slug']),
    ('installer_registration', 'manager.views.installer_registration', ['event_slug']),
    ('attendee_registration_print_code', 'manager.views.attendee_registration_print_code', ['event_slug']),
    ('add_registration_people', 'manager.views.add_registration_people', ['event_slug']),
    ('reports', 'manager.views.reports', ['event_slug']),
    ('add_reviewer', 'manager.views.add_reviewer', ['event_slug']),
    ('add_room', 'manager.views.add_or_edit_room', ['event_slug']),
    ('delete_room', 'manager.views.delete_room', ['event_slug', 'room_id']),
    ('edit_room', 'manager.views.add_or_edit_room', ['event_slug', 'room_id']),
    ('rooms_list', 'manager.views.rooms_list', ['event_slug']),
    ('schedule', 'manager.views.schedule', ['event_slug']),
    ('view_ticket', 'manager.views.view_ticket', ['event_slug'])
]
EVENT_URL_NAMES = [data[0] for data in EVENT_URLS_DATA]

# All
ALL_URLS_DATA = AUTOCOMPLETE_URLS_DATA + EVENT_URLS_DATA

ALL_URL_NAMES = ACCOUNTS_URL_NAMES + \
    AUTOCOMPLETE_URL_NAMES + \
    ALL_ADMIN_URLS_NAMES + \
    ALL_API_URL_NAMES + \
    EVENT_URL_NAMES
