# pylint: disable=broad-except
# pylint: disable=too-many-lines
import datetime
import io
import itertools
import json
import logging
import os
import re
import uuid
from smtplib import SMTPException
from urllib.parse import urlparse

import pyqrcode
import svglue
from allauth.utils import build_absolute_uri
from cairosvg import svg2pdf  # pylint: disable=no-member,no-name-in-module
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.forms import HiddenInput, modelformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_time
from django.utils.formats import date_format, localize
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as _noop
from django.utils.translation import ugettext
from djqscsv import render_to_csv_response
from lxml import etree

from manager.forms import (ActivityForm, ActivityProposalForm,
                           AttendeeRegistrationByCollaboratorForm,
                           AttendeeRegistrationForm,
                           AttendeeRegistrationFromUserForm,
                           AttendeeSearchForm, CollaboratorRegistrationForm,
                           ContactForm, ContactMessageForm, EventDateForm,
                           EventDateModelFormset, EventForm,
                           EventImageCroppingForm, EventUserRegistrationForm,
                           EventUserSearchForm, HardwareForm,
                           ImageCroppingForm, InstallationForm,
                           InstallerRegistrationForm, RejectForm, RoomForm,
                           ActivityDummyForm)
from manager.models import (Activity, Attendee, AttendeeAttendanceDate,
                            Collaborator, Contact, ContactMessage, Event,
                            EventDate, EventUser, EventUserAttendanceDate,
                            Hardware, Installation, InstallationMessage,
                            Installer, Organizer, Room, Reviewer, EventTag,
                            ActivityType)
from manager.security import (are_activities_public, add_attendance_permission,
                              add_organizer_permissions, is_activity_public, is_collaborator,
                              is_collaborator_or_installer, is_installer,
                              is_organizer, is_reviewer, user_passes_test, is_speaker)
from manager.utils.report import count_by

from .utils import email as utils_email
from .utils.forms import get_custom_fields

logger = logging.getLogger('eventol')


# Auxiliary functions
def update_event_info(event_slug, render_dict=None, event=None):
    event = get_object_or_404(Event, event_slug=event_slug)
    contacts = Contact.objects.filter(event=event)
    render_dict = render_dict or {}
    render_dict.update({
        'event_slug': event_slug,
        'event': event,
        'contacts': contacts
    })
    return render_dict


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def generate_ticket(user):
    ticket_data = user.get_ticket_data()
    ticket_template = svglue.load(
        file=os.path.join(
            settings.STATIC_ROOT, 'manager/img/ticket_template_p.svg'))
    ticket_template.set_text('event_name', ticket_data['event'].name[:24])
    ticket_template.set_text('event_date', localize(ticket_data['event_date']))
    place = json.loads(ticket_data['event'].place)
    if place.get("name"):
        ticket_template.set_text('event_place_name', place.get("name"))
        ticket_template.set_text(
            'event_place_address', place.get("formatted_address")[:50])
    else:
        ticket_template.set_text(
            'event_place_name', place.get("formatted_address")[:50])
        ticket_template.set_text('event_place_address', '')

    ticket_template.set_text('ticket_type', str(_("General Ticket")))
    qr_code = pyqrcode.create(str(ticket_data['ticket']))
    code = io.BytesIO()
    qr_code.png(code, scale=7, quiet_zone=0)
    ticket_template.set_image('qr_code', code.getvalue(), mimetype='image/png')
    ticket_template.set_text(
        'eventUser_PK', str(ticket_data['ticket'])
    )
    ticket_template.set_text('eventUser_email', ticket_data['email'])

    exists_first_name = ticket_data['first_name'] is not None
    exists_last_name = ticket_data['last_name'] is not None
    if exists_first_name or exists_last_name:
        user_name_l1 = '{} {}'.format(
            ticket_data['first_name'], ticket_data['last_name'])
        user_name_l2 = ''
        if len(user_name_l1) > 30:
            user_name_l1 = ticket_data['first_name'][:30]
            user_name_l2 = ticket_data['last_name'][:30]
    elif ticket_data.nickname is not None:
        user_name_l1 = ticket_data['nickname'][:30]
        user_name_l2 = ''
    elif ticket_data['email'] is not None:
        user_name_l1 = ticket_data['email'][:30]
        user_name_l2 = ''

    ticket_template.set_text('eventUser_name_l1', user_name_l1)
    ticket_template.set_text('eventUser_name_l2', user_name_l2)
    # pylint: disable=protected-access
    return etree.tostring(ticket_template._doc, encoding='utf8', method='xml')


def send_event_ticket(user):
    ticket_svg = generate_ticket(user)
    ticket_data = user.get_ticket_data()
    try:
        utils_email.send_ticket_email(ticket_data, ticket_svg)
        ticket_data['ticket'].sent = True
        ticket_data['ticket'].save()
    except SMTPException as error:
        logger.error(error)
        ticket_data['ticket'].sent = False
        ticket_data['ticket'].save()
        raise error


def create_organizer(event_user):
    organizer = Organizer.objects.filter(event_user=event_user).first()
    if organizer is None:
        organizer = Organizer.objects.create(event_user=event_user)
    add_organizer_permissions(organizer.event_user.user)
    organizer.save()
    return organizer


def index(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    if event.external_url:
        return redirect(event.external_url)

    activities_list = Activity.objects.filter(event=event, status=2) \
        .exclude(image__isnull=True) \
        .exclude(is_dummy=True) \
        .distinct()

    dates = EventDate.objects.filter(event=event)

    render_dict = {
        'activities': activities_list,
        'dates': dates,
        'tags': event.tags.all()
    }

    template_path = 'event/index.html'
    if event.template:
        template_path = event.template.name

    return render(
        request,
        template_path,
        update_event_info(
            event_slug,
            render_dict,
            event
        )
    )


def event_tag_index(request, tag):
    event_tag = get_object_or_404(EventTag, slug=tag)
    return render(request, 'event/tag_index.html', {'tag': event_tag})


def event_view(request, event_slug, html='index.html'):
    return render(
        request,
        html,
        update_event_info(
            event_slug
        )
    )


def home(request):
    if 'registration_event_slug' in request.session and request.user.is_authenticated():
        event_slug = request.session.pop('registration_event_slug')
        role = request.session.pop('registration_role')
        event_index = reverse(
            '{}_registration'.format(role),
            args=[event_slug])
        return redirect(event_index)
    return render(request, 'index.html')


@login_required
@user_passes_test(is_installer, 'installer_registration')
def installation(request, event_slug):
    installation_form = InstallationForm(
        event_slug, request.POST or None, prefix='installation')
    hardware_form = HardwareForm(request.POST or None, prefix='hardware')
    forms = [installation_form, hardware_form]
    errors = []
    if request.POST:
        if hardware_form.is_valid() and installation_form.is_valid():
            try:
                hardware = hardware_form.save()
                install = installation_form.save()
                install.hardware = hardware
                event = get_object_or_404(Event, event_slug=event_slug)
                install.event = event
                install.installer = EventUser.objects \
                    .filter(user=request.user).filter(event=event).first()
                install.save()
                # Send post-install email if its defined
                postinstall_email = InstallationMessage.objects \
                    .filter(event=event).first()
                if postinstall_email:
                    try:
                        utils_email.send_installation_email(
                            event.name, postinstall_email, install.attendee)
                    except SMTPException as error:
                        logger.error(error)
                        messages.error(request, _("The email couldn't sent successfully, \
                                                  please retry later or contact a organizer"))
                messages.success(
                    request,
                    _(
                        "The installation has been registered successfully. "
                        "Happy Hacking!"
                    )
                )
                event_index_url = reverse(
                    'index',
                    args=[event_slug]
                )
                return redirect(event_index_url)
            except Exception as error_message:
                logger.error(error_message)
                if hardware is not None:
                    Hardware.delete(hardware)
                if install is not None:
                    Installation.delete(install)
        messages.error(
            request,
            _("The installation couldn't be registered (check form errors)")
        )
        errors = get_forms_errors(forms)

    return render(
        request,
        'installation/installation-form.html',
        update_event_info(
            event_slug,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def manage_attendance(request, event_slug):
    attendee_form = AttendeeSearchForm(
        event_slug,
        request.POST or None
    )
    collaborator_form = EventUserSearchForm(
        event_slug,
        request.POST or None
    )
    forms = [attendee_form, collaborator_form]
    errors = []
    if request.POST:
        if attendee_form.is_valid():
            attendee = attendee_form.cleaned_data['attendee']
            if attendee:
                if attendee.attended_today():
                    messages.success(
                        request,
                        _(
                            'The attendee has already been registered '
                            'correctly.'
                        )
                    )
                else:
                    attendance_date = AttendeeAttendanceDate()
                    attendance_date.attendee = attendee
                    attendance_date.mode = '3'
                    attendance_date.save()
                    messages.success(
                        request,
                        _(
                            'The attendee has been successfully registered. '
                            'Happy Hacking!'
                        )
                    )
                    return redirect(
                        reverse(
                            'manage_attendance',
                            args=[event_slug]
                        )
                    )
        if collaborator_form.is_valid():
            event_user = collaborator_form.cleaned_data['event_user']
            if event_user:
                if event_user.attended_today():
                    messages.success(
                        request,
                        _(
                            'The collaborator has already been registered '
                            'correctly.'
                        )
                    )
                else:
                    attendance_date = EventUserAttendanceDate()
                    attendance_date.event_user = event_user
                    attendance_date.mode = '3'
                    attendance_date.save()
                    messages.success(
                        request,
                        _(
                            'The collaborator has been successfully '
                            'registered. Happy Hacking!'
                        )
                    )
                return redirect(
                    reverse(
                        'manage_attendance',
                        args=[event_slug]
                    )
                )

        messages.error(
            request,
            _(
                'There was a problem registering the attendee. '
                'Please try again.'
            )
        )

        errors = get_forms_errors(forms)

    return render(
        request,
        'registration/attendee/search.html',
        update_event_info(
            event_slug,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendance_by_ticket(request, event_slug, ticket_code):
    attendee = Attendee.objects.filter(ticket__code=ticket_code)
    if not attendee:
        attendee = EventUser.objects.filter(ticket__code=ticket_code)

    if attendee:
        attendee = attendee.get()
        if attendee.attended_today():
            messages.success(
                request,
                _('The attendee has already been registered correctly.'))
        else:
            if hasattr(attendee, 'user'):
                attendance_date = EventUserAttendanceDate()
                attendance_date.event_user = attendee
            else:
                attendance_date = AttendeeAttendanceDate()
                attendance_date.attendee = attendee
            attendance_date.mode = '2'
            attendance_date.save()
            messages.success(
                request,
                _(
                    'The attendee has been successfully registered. '
                    'Happy Hacking!'
                )
            )
    else:
        messages.error(request, _("The user isn't registered for this event."))

    return redirect(
        reverse(
            'manage_attendance',
            args=[event_slug]
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_organizer(request, event_slug):
    form = EventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['event_user']
            if event_user:
                organizer = create_organizer(event_user)
                messages.success(
                    request,
                    _(
                        "%s has been successfully added as an Organizer." \
                        % organizer.event_user.user.username
                    )
                )
            return redirect(
                reverse(
                    'add_organizer',
                    args=[event_slug]
                )
            )

        messages.error(
            request,
            _(
                'Something went wrong (please check form errors)'
            )
        )

    organizers = Organizer.objects.filter(
        event_user__event__event_slug=event_slug
    )
    return render(
        request,
        'event/organizers.html',
        update_event_info(
            event_slug,
            {'form': form, 'organizers': organizers}
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_registration_people(request, event_slug):
    form = EventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['event_user']
            if event_user:
                Collaborator.objects.get_or_create(event_user=event_user)
                add_attendance_permission(event_user.user)
                messages.success(
                    request,
                    _(
                        "%s has been successfully added to manage attendance." \
                        % event_user.user.username
                    )
                )
            return redirect(
                reverse(
                    'add_registration_people',
                    args=[event_slug]
                )
            )

        messages.error(
            request,
            _(
                'Something went wrong (please check form errors)'
            )
        )

    content_type = ContentType.objects.get_for_model(Attendee)
    if Permission.objects.filter(
            codename='can_take_attendance', content_type=content_type).exists():
        permission = Permission.objects.get(
            codename='can_take_attendance',
            content_type=content_type
        )
        registration_people = Collaborator.objects.filter(
            event_user__user__user_permissions=permission,
            event_user__event__event_slug=event_slug
        )
    else:
        registration_people = []

    return render(
        request,
        'event/registration_people.html',
        update_event_info(
            event_slug,
            {'form': form, 'registration_people': registration_people}
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_reviewer(request, event_slug):
    """Add reviewer access to Colaborator user."""
    form = EventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['event_user']
            if event_user:
                Reviewer.objects.get_or_create(event_user=event_user)
                messages.success(
                    request, _("{} has been successfully added as reviewer.".format(
                        event_user.user.username))
                )
            return redirect(reverse('add_reviewer', args=[event_slug]))
        messages.error(request, _('Something went wrong (please check form errors)'))
    reviewers = Reviewer.objects.filter(event_user__event__event_slug=event_slug)
    return render(
        request, 'event/review_people.html',
        update_event_info(event_slug, {'form': form, 'review_people': reviewers})
    )


@login_required
@user_passes_test(is_collaborator_or_installer, 'collaborator_registration')
def registration_from_installation(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    installation_url = reverse(
        'installation',
        args=[event_slug]
    )
    render_template = 'registration/attendee/from-installation.html'
    return process_attendee_registration(
        request,
        event=event,
        return_url=installation_url,
        render_template=render_template
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator_or_installer, 'collaborator_registration')
def registration_by_collaborator(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    manage_attendance_url = reverse(
        'manage_attendance',
        args=[event_slug]
    )
    render_template = 'registration/attendee/by-collaborator.html'
    return process_attendee_registration(
        request,
        event=event,
        return_url=manage_attendance_url,
        render_template=render_template
    )


def process_attendee_registration(request, event, return_url, render_template):
    # Verify date, allow only on event day or after
    eventdate = EventDate.objects.filter(
        event=event, date__lte=timezone.localdate()).order_by('-date').first()
    form = AttendeeRegistrationByCollaboratorForm(
        request.POST or None,
        initial={'event': event}
    )
    if eventdate:
        if request.POST:
            if form.is_valid():
                email = form.cleaned_data["email"]
                if Attendee.objects.filter(event=event, email__iexact=email).exists():
                    messages.error(
                        request,
                        _(
                            'The attendee is already registered for this event, '
                            'use correct form'
                        )
                    )
                    return redirect(return_url)
                try:
                    attendee = form.save()
                    attendance_date = AttendeeAttendanceDate.objects.create(
                        attendee=attendee,
                        mode='4'
                    )
                    messages.success(
                        request,
                        _(
                            'The attendee was successfully registered. '
                            'Happy Hacking!'
                        )
                    )
                    return redirect(return_url)
                except Exception as error_message:
                    logger.error(error_message)
                    try:
                        if attendee is not None:
                            Attendee.objects.delete(attendee)
                        if attendance_date is not None:
                            AttendeeAttendanceDate.objects.delete(attendance_date)
                    except Exception:
                        pass
            messages.error(
                request,
                _(
                    "The attendee couldn't be registered (check form errors)"
                )
            )
    else:
        messages.error(request, _('You can only register an attendance \
                                  at the day of the event or after'))
    return render(
        request,
        render_template,
        update_event_info(
            event.event_slug,
            {'form': form}
        )
    )

@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator_or_installer, 'collaborator_registration')
def attendee_registration_print_code(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    self_registration_url = request.build_absolute_uri(reverse(
        'attendee_registration_by_self',
        args=[event_slug, event.registration_code]
    ))
    qr_code = pyqrcode.create(self_registration_url)
    code = io.BytesIO()
    qr_code.png(code, scale=9, quiet_zone=0)
    data = {
        'event_name': event.name,
        'qr_code': code.getvalue(),
        'self_registration_title': ugettext('Self-registration'),
        'self_registration_text': ugettext('Scan this QR code to register yourself'),
    }
    template = {
        'text': {
            'event_name_1': data['event_name'],
            'self_registration_title_1': data['self_registration_title'],
            'self_registration_text_1': data['self_registration_text'],
            'event_name_2': data['event_name'],
            'self_registration_title_2': data['self_registration_title'],
            'self_registration_text_2': data['self_registration_text'],
        },
        'image': {
            'qr_code_1': data['qr_code'],
            'qr_code_2': data['qr_code'],
        },
    }

    registration_code_template = svglue.load(
        file=os.path.join(settings.STATIC_ROOT, 'manager/img/registration_code_template_p.svg')
    )
    for type_name, data in template.items():
        if type_name == 'text':
            for key, value in data.items():
                registration_code_template.set_text(key, value)
        else:
            # image
            for key, value in data.items():
                registration_code_template.set_image(key, value, mimetype='image/png')
    # pylint: disable=protected-access
    registration_code_svg = etree.tostring(
        registration_code_template._doc, encoding='utf8', method='xml')
    response = HttpResponse(
        svg2pdf(bytestring=registration_code_svg), content_type='application/pdf')
    response["Content-Disposition"] = 'filename=Registration-code-{event}.pdf'.format(
        event=event.event_slug)
    return response


def attendee_registration_by_self(request, event_slug, event_registration_code):
    event_index_url = reverse('index', args=[event_slug])
    event = Event.objects.filter(
        event_slug=event_slug, registration_code=event_registration_code
    ).first()
    if not event:
        messages.error(
            request, _('The registration code does not seems to be valid for this event'))
        return redirect(event_index_url)
    # Check if today is a valid EventDate
    try:
        EventDate.objects.get(event=event, date=timezone.localdate())
    except EventDate.DoesNotExist:
        messages.error(request, _('You can only register by yourself on the event date'))
        return redirect(event_index_url)
    form = AttendeeRegistrationByCollaboratorForm(
        request.POST or None,
        initial={'event': event}
    )
    if request.POST:
        attendee_email_raw = request.POST.get('email')
        try:
            validate_email(attendee_email_raw)
            attendee = Attendee.objects.filter(
                event=event, email__iexact=attendee_email_raw).first()
        except ValidationError:
            attendee = None
        mode = None
        if attendee:
            mode = '3'
            messages.info(
                request,
                _(
                    'You are already registered!'
                )
            )
        elif form.is_valid():
            mode = '1'
            attendee = form.save()
        if attendee:
            if attendee.attended_today():
                messages.info(request, 'You are already registered and present! Go have fun')
                return redirect(event_index_url)
            try:
                attendance_date = AttendeeAttendanceDate()
                attendance_date.mode = mode
                attendance_date.attendee = attendee
                attendance_date.save()
                messages.success(
                    request,
                    _(
                        'You are now marked as present in the event, have fun!'
                    )
                )
                return redirect(event_index_url)
            except Exception as error_message:
                logger.error(error_message)
                try:
                    if attendee is not None:
                        Attendee.objects.delete(attendee)
                    if attendance_date is not None:
                        AttendeeAttendanceDate.objects.delete(attendance_date)
                except Exception:
                    pass
        messages.error(
            request,
            _(
                "You couldn't be registered (check form errors)"
            )
        )
    return render(
        request,
        'registration/attendee/by-self.html',
        update_event_info(
            event_slug,
            {
                'form': form,
                'event_registration_code': event_registration_code,
            }
        )
    )


def attendance_by_autoreadqr(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event_index_url = reverse(
        'index',
        args=[event_slug]
    )
    event_registration_code = request.GET.get('event_registration_code', '')
    user = request.user
    # Show page w/ reg code for collaborators/organizers
    if not event_registration_code \
            and user.is_authenticated() \
            and (
                    is_collaborator(user, event_slug=event_slug)
                    or is_organizer(user, event_slug=event_slug)
            ):
        return redirect(
            '{url}/?event_registration_code={event_registration_code}'.format(
                url=reverse('attendance_by_autoreadqr', args=[event_slug]),
                event_registration_code=event.registration_code
            )
        )

    # Check if reg code is valid
    if not event_registration_code \
        or not Event.objects.filter(
                event_slug=event_slug, registration_code=event_registration_code).exists():
        messages.error(request, _('The registration code does \
                                  not seems to be valid for this event'))
        return redirect(event_index_url)

    # Check if today is a valid EventDate
    if not EventDate.objects.filter(event=event, date=timezone.localdate()).exists():
        messages.error(request, _('Auto-reading QR codes is only available at the event date'))
        return redirect(event_index_url)

    # Check ticket
    ticket_code = request.GET.get('ticket', '')
    if ticket_code:
        event_user = EventUser.objects.filter(event=event, ticket__code=ticket_code)
        attendee = Attendee.objects.filter(event=event, ticket__code=ticket_code)
        if event_user.exists():
            event_user = event_user.first()
            attendance = EventUserAttendanceDate.objects.filter(
                event_user=event_user, date__date=timezone.localdate())
            if attendance.exists():
                messages.info(
                    request, _('You are already registered and present! Go have fun'))
            else:
                EventUserAttendanceDate.objects.create(event_user=event_user, mode='2')
                messages.success(
                    request, _('You are now marked as present in the event, have fun!'))
        elif attendee.exists():
            attendee = attendee.first()
            attendance = AttendeeAttendanceDate.objects.filter(
                attendee=attendee, date__date=timezone.localdate())
            if attendance.exists():
                messages.info(
                    request, _('You are already registered and present! Go have fun'))
            else:
                AttendeeAttendanceDate.objects.create(attendee=attendee, mode='2')
                messages.success(
                    request, _('You are now marked as present in the event, have fun!'))
        else:
            messages.error(request, _('The ticket code is not valid for this event'))

    return render(
        request,
        'registration/attendee/by-autoreadqr.html',
        update_event_info(
            event_slug,
            {
                'event_registration_code': event_registration_code,
            }
        )
    )


def contact(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    contact_message = ContactMessage()
    form = ContactMessageForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            contact_message = form.save()
            email = EmailMultiAlternatives()
            email.subject = _noop('[eventoL] Contact message from {name}').format(
                name=contact_message.name)
            email.body = str(contact_message)
            email.from_email = contact_message.email
            email.to = [event.email]
            email.extra_headers = {'Reply-To': contact_message.email}
            email.send(fail_silently=False)
            event = get_object_or_404(Event, event_slug=event_slug)
            contact_message.event = event
            contact_message.save()
            messages.success(
                request,
                _(
                    'The message has been sent. You will receive a reply by '
                    'email'
                )
            )
            return redirect(
                reverse(
                    'index',
                    args=[event_slug]
                )
            )
        messages.error(
            request,
            _(
                'There was a problem sending your message. '
                'Please try again in a few minutes.'
            )
        )

    return render(
        request,
        'contact-message.html',
        update_event_info(
            event_slug,
            {'form': form},
            event
        )
    )

# pylint: disable=too-many-locals
def reports(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event_dates = EventDate.objects.filter(event=event)
    confirmed_attendees_count, not_confirmed_attendees_count, speakers_count = 0, 0, 0

    installers = Installer.objects.filter(event_user__event=event)
    installations = Installation.objects.filter(attendee__event=event)
    talks = Activity.objects.filter(event=event).filter(is_dummy=False)
    collaborators = Collaborator.objects.filter(event_user__event=event)
    collaborators_event_users = [collaborator.event_user for collaborator in list(collaborators)]
    installers_event_users = [installer.event_user for installer in list(installers)]
    attendees = Attendee.objects.filter(event=event)

    attendees_attendance = AttendeeAttendanceDate.objects.filter(
        attendee__event=event).order_by('attendee').distinct()
    confirmed_attendees_count = attendees_attendance.count()
    not_confirmed_attendees_count = attendees.count() - confirmed_attendees_count

    confirmed_collaborators_count = EventUserAttendanceDate.objects.filter(
        event_user__event=event, event_user__in=collaborators_event_users
        ).order_by('event_user').distinct().count()
    not_confirmed_collaborators = collaborators.count() - confirmed_collaborators_count
    confirmed_installers_count = EventUserAttendanceDate.objects.filter(
        event_user__event=event, event_user__in=installers_event_users
        ).order_by('event_user').distinct().count()
    not_confirmed_installers_count = installers.count() - confirmed_installers_count

    speakers = []
    for talk in talks:
        speakers.append(talk.speakers_names.split(','))
    speakers_count = len(set(itertools.chain.from_iterable(speakers)))

    attendance_by_date = {}
    for event_date in event_dates:
        attendance_for_date = AttendeeAttendanceDate.objects.filter(
            attendee__event=event, date__date=event_date.date).order_by('attendee').distinct()
        attendance_by_date[event_date.date.strftime("%Y-%m-%d")] = count_by(
            attendance_for_date, lambda attendance: attendance.date.hour - 3)

    template_dict = {
        'event_dates': [event_date.date.strftime("%Y-%m-%d") for event_date in event_dates],
        'confirmed_attendees_count': confirmed_attendees_count,
        'not_confirmed_attendees_count': not_confirmed_attendees_count,
        'confirmed_collaborators_count': confirmed_collaborators_count,
        'not_confirmed_collaborators_count': not_confirmed_collaborators,
        'confirmed_installers_count': confirmed_installers_count,
        'not_confirmed_installers_count': not_confirmed_installers_count,
        'speakers_count': speakers_count,
        'organizers_count': Organizer.objects.filter(event_user__event=event).count(),
        'activities_count': talks.count(),
        'installations_count': Installation.objects.filter(attendee__event=event).count(),
        'installers_for_level': count_by(installers, lambda inst: inst.level),
        'installers_count': installers.count(),
        'installation_for_software': count_by(installations, lambda inst: inst.software.name),
        'registered_in_time': count_by(
            attendees, lambda attendee: attendee.registration_date.date()),
        'attendance_by_date': attendance_by_date
    }

    return render(
        request,
        'reports/dashboard.html',
        update_event_info(
            event_slug,
            render_dict=template_dict
        )
    )
# pylint: enable=too-many-locals


# pylint: disable=too-many-arguments
@login_required
def generic_registration(request, event_slug,
                         registration_model, new_role_form,
                         msg_success, msg_error, template):
    event = get_object_or_404(Event, event_slug=event_slug)

    if not event.registration_is_open:
        return render(
            request,
            'registration/closed-registration.html',
            update_event_info(event_slug)
        )

    errors = []
    event_user = EventUser.objects.filter(event=event, user=request.user).first()
    if not event_user:
        event_user = EventUser(event=event, user=request.user)
        event_user.save()

    new_role = registration_model.objects.filter(event_user=event_user)

    if new_role:
        # Ya esta registrado con ese "rol"
        messages.error(request, _("You are already registered for this event"))
        return redirect(reverse("index", args=[event_slug]))

    new_role = registration_model(event_user=event_user)
    if request.POST:
        event_user_form = EventUserRegistrationForm(request.POST, instance=event_user)
        new_role_form = new_role_form(request.POST, instance=new_role)
        forms = [event_user_form, new_role_form]
        if event_user_form.is_valid() and new_role_form.is_valid():
            try:
                event_user = event_user_form.save()
                new_role = new_role_form.save()
                new_role.event_user = event_user
                new_role.save()
                messages.success(request, msg_success)
                return redirect(
                    reverse(
                        'index',
                        args=[event_slug]
                    )
                )
            except Exception as error_message:
                logger.error(error_message)
        messages.error(request, msg_error)
    else:
        event_user_form = EventUserRegistrationForm(instance=event_user)
        new_role_form = new_role_form(instance=new_role)
        forms = [event_user_form, new_role_form]

    return render(
        request,
        template,
        update_event_info(
            event_slug,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )
# pylint: enable=too-many-arguments

def get_email_confirmation_url(request, event_slug, attendee_id, token):
    url = reverse(
        "attendee_confirm_email",
        args=[event_slug, attendee_id, token])
    ret = build_absolute_uri(
        request,
        url)
    return ret


def attendee_registration(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)

    if not event.registration_is_open or event.registration_closed:
        return render(
            request,
            'registration/closed-registration.html',
            update_event_info(
                event_slug,
                event=event
            )
        )

    if request.user.is_authenticated():
        event_user = EventUser.objects.filter(event=event, user=request.user).first()
        if not event_user:
            event_user = EventUser(event=event, user=request.user)
            event_user.save()
        attendee = Attendee.objects.filter(event_user=event_user)
        if attendee.exists():
            messages.error(request, _("You are already registered for this event"))
            return redirect(reverse("index", args=[event_slug]))

        attendee = Attendee(
            event_user=event_user, first_name=event_user.user.first_name,
            last_name=event_user.user.last_name, email=event_user.user.email,
            event=event_user.event, nickname=event_user.user.username
        )
        attendee_form = AttendeeRegistrationFromUserForm(
            request.POST or None, instance=attendee)
    else:
        attendee_form = AttendeeRegistrationForm(request.POST or None,
                                                 initial={'event': event})

    if not event.use_installations:
        attendee_form.fields['is_installing'].widget = HiddenInput()

    if request.POST:
        if attendee_form.is_valid():
            try:
                attendee = attendee_form.save(commit=False)
                attendee.event = event
                attendee.registration_date = timezone.now()
                attendee.email_token = uuid.uuid4().hex
                attendee.customFields = get_custom_fields(event, request.POST)
                attendee.save()

                confirm_url = get_email_confirmation_url(
                    request,
                    event_slug,
                    attendee.id,
                    attendee.email_token)

                if request.user.is_authenticated():
                    return redirect(confirm_url)
                body_text = _noop(
                    'Hi! You are receiving this message because you have'
                    'registered to attend to '
                    '{event_name}, being held on {event_dates}.\n\n'
                    'Please follow this link to confirm your email address'
                    'and we will send you your '
                    'ticket:\n'
                    '{confirm_url}\n\n'
                    'If you encounter any issue, please contact the event organizer in '
                    '{event_contact_url}.\n\n'
                    'Happily yours,\n'
                    '{event_name} and eventoL team'
                ).format(
                    event_name=event.name,
                    event_dates=', '.join([
                        date_format(eventdate.date, format='SHORT_DATE_FORMAT', use_l10n=True)
                        for eventdate in EventDate.objects.filter(event=event)
                    ]),
                    event_contact_url=reverse('contact', args=[event_slug]),
                    confirm_url=confirm_url
                )
                body_html = _noop(
                    '<p>Hi! You are receiving this message because you have'
                    'registered to attend to <strong>'
                    '{event_name}</strong>, being held on {event_dates}.</p>\n'
                    '<p>Please <em>follow this link to confirm your email'
                    'address</em> and we will send you your '
                    'ticket:<br />\n'
                    '<a href="{confirm_url}">{confirm_url}</a></p>\n'
                    '<p>If you encounter any issue, please contact the event organizer in '
                    '<a href="{event_contact_url}">{event_contact_url}</a>.</p>\n'
                    '<p>Happily yours,<br />\n'
                    '{event_name} and <em>eventoL</em> team</p>'
                ).format(
                    event_name=event.name,
                    event_dates=', '.join([
                        date_format(eventdate.date, format='SHORT_DATE_FORMAT', use_l10n=True)
                        for eventdate in EventDate.objects.filter(event=event)
                    ]),
                    event_contact_url=reverse('contact', args=[event_slug]),
                    confirm_url=confirm_url
                )

                email = EmailMultiAlternatives()
                email.subject = _('[eventoL] Please confirm your email')
                email.body = body_text
                email.attach_alternative(body_html, 'text/html')
                email.from_email = settings.EMAIL_FROM
                email.to = [attendee.email]
                email.extra_headers = {'Reply-To': settings.EMAIL_FROM}
                email.send(fail_silently=False)
                return redirect(
                    reverse(
                        'attendee_email_sent',
                        args=[event_slug]
                    )
                )
            except Exception as error_message:
                logger.error(error_message)
                if attendee is not None:
                    attendee.delete()

        messages.error(request, _('There is a problem with the registration (check form errors)'))

    return render(
        request,
        'registration/attendee-registration.html',
        update_event_info(
            event_slug,
            {
                'form': attendee_form,
                'errors': get_forms_errors([attendee_form]),
                'multipart': False
            },
            event=event
        )
    )


def attendee_confirm_email(request, event_slug, attendee_id, token):
    attendee = Attendee.objects.get(pk=attendee_id)
    title = _("Email verification")
    message = _(
        "We've sent you your ticket to your email! In case it doesn't arrive, \
        don't worry! You're already registered and we'll ask for your email address.")
    if not attendee.email_confirmed:
        if attendee.email_token == token:
            try:
                attendee.email_confirmed = True
                attendee.save()
                send_event_ticket(attendee)
            except SMTPException as error:
                logger.error(error)
                messages.error(
                    request,
                    _("The email couldn't sent successfully, \
                      please retry later or contact a organizer"))
            except Exception as error_message:
                logger.error(error_message)
        else:
            message = _('The verification URL is invalid. Try again.')

    return render(
        request,
        'registration/attendee/ticket-sent.html',
        {
            'message': message,
            'title': title,
            'event_slug': event_slug
        }
    )


def installer_registration(request, event_slug):
    if not request.user.is_authenticated():
        request.session['registration_event_slug'] = event_slug
        request.session['registration_role'] = 'installer'
    msg_success = _("You have successfully registered as an installer")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/installer-registration.html'
    return generic_registration(
        request,
        event_slug,
        Installer,
        InstallerRegistrationForm,
        msg_success,
        msg_error,
        template
    )


def collaborator_registration(request, event_slug):
    if not request.user.is_authenticated():
        request.session['registration_event_slug'] = event_slug
        request.session['registration_role'] = 'collaborator'
    msg_success = _("You have successfully registered as a collaborator")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/collaborator-registration.html'
    return generic_registration(
        request,
        event_slug,
        Collaborator,
        CollaboratorRegistrationForm,
        msg_success,
        msg_error,
        template
    )

# pylint: disable=too-many-branches
@login_required
def create_event(request):
    event_form = EventForm(request.POST or None, prefix='event')
    contacts_formset = modelformset_factory(Contact, form=ContactForm, can_delete=True)

    # pylint: disable=unexpected-keyword-arg
    contacts_formset = contacts_formset(
        request.POST or None, prefix='contacts-form', queryset=Contact.objects.none())
    # pylint: enable=unexpected-keyword-arg

    event_date_formset = modelformset_factory(
        EventDate, form=EventDateForm, formset=EventDateModelFormset, can_delete=True)

    # pylint: disable=unexpected-keyword-arg
    event_date_formset = event_date_formset(
        request.POST or None,
        prefix='event-date-form',
        queryset=EventDate.objects.none()
    )
    # pylint: enable=unexpected-keyword-arg

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid() and event_date_formset.is_valid():
            organizer = None
            event_user = None
            the_event = None
            contacts = None
            event_dates = None
            try:
                the_event = event_form.save()
                event_user = EventUser.objects.create(user=request.user, event=the_event)
                organizer = create_organizer(event_user)
                contacts = contacts_formset.save(commit=False)
                event_dates = event_date_formset.save(commit=False)

                for a_contact in contacts:
                    a_contact.event = the_event
                    a_contact.save()

                for event_date in event_dates:
                    event_date.event = the_event
                    event_date.save()

                return redirect(reverse('event_add_image', args=[the_event.event_slug]))
            except Exception as error_message:
                logger.exception(error_message)
                try:
                    if organizer is not None:
                        Organizer.delete(organizer)
                    if event_user is not None:
                        EventUser.delete(event_user)
                    if the_event is not None:
                        Event.delete(the_event)
                    if contacts is not None:
                        for a_contact in list(contacts):
                            Contact.objects.delete(a_contact)
                    if event_dates is not None:
                        for event_date in list(event_dates):
                            EventDate.objects.delete(event_date)
                except Exception:
                    logger.exception("error creating event")


        messages.error(
            request,
            _('There is a problem with your event. Please check the form for errors.'))
    return render(request,
                  'event/create.html',
                  {'form': event_form, 'domain': request.get_host(),
                   'protocol': request.scheme, 'contacts_formset': contacts_formset,
                   'fields_dependencies': Event.get_fields_dependencies(),
                   'event_date_formset': event_date_formset})
# pylint: enable=too-many-branches


@login_required
@user_passes_test(is_organizer, 'index')
def edit_event(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event_form = EventForm(request.POST or None, prefix='event', instance=event)

    contacts_formset = modelformset_factory(Contact, form=ContactForm, can_delete=True)
    # pylint: disable=unexpected-keyword-arg
    contacts_formset = contacts_formset(
        request.POST or None, prefix='contacts-form',
        queryset=event.contacts.all())
    # pylint: enable=unexpected-keyword-arg

    event_date_formset = modelformset_factory(
        EventDate, form=EventDateForm,
        formset=EventDateModelFormset, can_delete=True)

    # pylint: disable=unexpected-keyword-arg
    event_date_formset = event_date_formset(
        request.POST or None, prefix='event-date-form',
        queryset=EventDate.objects.filter(event=event))
    # pylint: enable=unexpected-keyword-arg

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid() and event_date_formset.is_valid():
            try:
                the_event = event_form.save()
                contacts = contacts_formset.save(commit=False)
                event_dates = event_date_formset.save(commit=False)

                for a_contact in contacts:
                    a_contact.event = the_event

                for event_date in event_dates:
                    event_date.event = the_event

                contacts_formset.save()
                event_date_formset.save()

                return redirect(reverse('index', args=[the_event.event_slug]))
            except Exception as error_message:
                logger.error(error_message)

        messages.error(
            request, _("There is a problem with your event. Please check the form for errors."))
    return render(
        request,
        'event/create.html',
        update_event_info(
            event_slug,
            {
                'form': event_form,
                'domain': request.get_host(),
                'protocol': request.scheme,
                'contacts_formset': contacts_formset,
                'event_date_formset': event_date_formset,
                'fields_dependencies': Event.get_fields_dependencies()
            }
        )
    )


@login_required
def view_ticket(request, event_slug):
    event_user = EventUser.objects.filter(
        event__event_slug=event_slug).filter(user=request.user).first()
    if event_user:
        ticket = generate_ticket(event_user)
        response = HttpResponse(svg2pdf(bytestring=ticket), content_type='application/pdf')
        response["Content-Disposition"] = 'filename=Ticket-' + str(event_user.ticket.code) + '.pdf'
        return response
    messages.error(request, "You are not registered for this event")
    return redirect(reverse("index", args=[event_slug]))


@login_required
@user_passes_test(is_organizer, 'index')
def draw(request, event_slug):
    users = [
        str(attendance_date.attendee) for attendance_date in
        AttendeeAttendanceDate.objects.filter(
            attendee__event__event_slug=event_slug,
            date__date=timezone.localdate()
        )
    ]
    return render(
        request,
        'event/draw.html',
        update_event_info(
            event_slug,
            {'eventusers': users, 'eventusersjson': json.dumps(users)}
        )
    )


@login_required
@user_passes_test(is_reviewer, 'index')
def activity_dummy(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event_user = get_object_or_404(EventUser, user=request.user, event=event)
    activity_type, __ = ActivityType.objects.get_or_create(name=_('Dummy'))

    activity = Activity(
        event=event, status='2', owner=event_user,
        is_dummy=True, activity_type=activity_type
    )
    activity_form = ActivityDummyForm(request.POST or None, instance=activity)
    if request.POST:
        if activity_form.is_valid():
            try:
                activity = activity_form.save()
                return redirect(
                    reverse(
                        'activities',
                        args=[event_slug]
                    )
                )
            except Exception as error_message:
                logger.error(error_message)

        messages.error(request, _("There was a problem submitting the proposal. \
                                  Please check the form for errors."))

    return render(
        request,
        'activities/proposal.html',
        update_event_info(
            event_slug,
            {'form': activity_form, 'errors': [], 'multipart': True},
            event=event
        )
    )


@login_required
def activity_proposal(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)

    if not event.activity_proposal_is_open:
        messages.error(request,
                       _(
                           "The activity proposal is already closed or the event \
                           is not accepting proposals through this page. Please \
                           contact the Event Organization Team to submit it."))
        return redirect(reverse('index', args=[event_slug]))

    event_user, created = EventUser.objects.get_or_create(user=request.user, event=event)
    if created:
        # register the user in the event
        logger.info(
            "The user %s is proposing an activity in event: %s. Creating EventUser and Attendee",
            event_user.user.email, event)
        Attendee(event_user=event_user, first_name=event_user.user.first_name,
                 last_name=event_user.user.last_name, email=event_user.user.email,
                 event=event_user.event, nickname=event_user.user.username
                 )
    activity = Activity(event=event, status='1', owner=event_user)
    activity_form = ActivityProposalForm(
        request.POST or None, request.FILES or None, instance=activity)

    if request.POST:
        if activity_form.is_valid():
            try:
                activity = activity_form.save()
                return redirect(
                    reverse(
                        'image_cropping',
                        args=[event_slug, activity.pk]
                    )
                )
            except Exception as error_message:
                logger.error(error_message)

        messages.error(request, _("There was a problem submitting the proposal. \
                                  Please check the form for errors."))

    return render(
        request,
        'activities/proposal.html',
        update_event_info(
            event_slug,
            {'form': activity_form, 'errors': [], 'multipart': True},
            event=event
        )
    )


@login_required
@user_passes_test(is_speaker, 'index')
def edit_activity_proposal(request, event_slug, activity_id):
    event = get_object_or_404(Event, event_slug=event_slug)

    if event.schedule_confirmed:
        messages.error(request,
                       _(
                           "The activity proposal edition is already closed or the event \
                           is not accepting proposals through this page. Please \
                           contact the Event Organization Team to submit it."))
        return redirect(reverse('index', args=[event_slug]))

    event_user = get_object_or_404(EventUser, user=request.user, event=event)
    activity = get_object_or_404(Activity, event=event, owner=event_user, pk=activity_id)
    activity_form = ActivityProposalForm(
        request.POST or None, request.FILES or None, instance=activity)

    if request.POST:
        if activity_form.is_valid():
            try:
                activity = activity_form.save()
                return redirect(
                    reverse(
                        'image_cropping',
                        args=[event_slug, activity.pk]
                    )
                )
            except Exception as error_message:
                logger.error(error_message)
        messages.error(request, _("There was a problem submitting the proposal. \
                                  Please check the form for errors."))
    return render(
        request,
        'activities/proposal.html',
        update_event_info(
            event_slug,
            {'form': activity_form, 'errors': [], 'multipart': True},
            event=event
        )
    )


def image_cropping(request, event_slug, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    form = ImageCroppingForm(request.POST or None, request.FILES, instance=activity)
    if request.POST:
        if form.is_valid():
            # If a new file is being upload
            if request.FILES:
                # If clear home_image is clicked, delete the image
                if request.POST.get('image-clear') or request.FILES:
                    form.cleaned_data['image'] = None
                # Save the changes and redirect to upload a new one or crop the new one
                activity = form.save()
                activity.save()
                messages.success(request, _("Please crop or upload a new image."))
                return redirect(
                    reverse(
                        'image_cropping',
                        args=[event_slug, activity.pk]
                    )
                )
            form.save()
            messages.success(request, _(
                "The proposal has been registered successfully! We'll contact \
                you at the provided email"))
            return redirect(
                reverse(
                    'activity_detail',
                    args=[event_slug, activity.pk]
                )
            )
        messages.error(request, _("The proposal couldn't be registered. Please \
        check the form for errors"))
    return render(
        request,
        'activities/image-cropping.html',
        update_event_info(
            event_slug,
            {'form': form}
        )
    )


def goto_next_or_continue(next_url, safe_continue=None):
    if next_url:
        url = urlparse(next_url)
        safe_url = re.sub(r'[^\w/\-]', '', url.path)
        safe_query = re.sub(r'[^\w/\-+=&]', '', url.query)
        try:
            return redirect(safe_url + '?' + safe_query)
        except Exception as error_message:
            logger.error(error_message)
    elif safe_continue:
        return redirect(safe_continue)
    raise Http404('I can not go anywhere, next and continue are empty')


@login_required
@user_passes_test(is_organizer, 'index')
def change_activity_status(request, event_slug, activity_id, status, justification=None):
    event = get_object_or_404(Event, event_slug=event_slug)
    activity = get_object_or_404(Activity, id=activity_id)
    activity.status = status
    activity.start_date = None
    activity.end_date = None
    activity.room = None
    activity.justification = justification
    activity.save()
    try:
        utils_email.send_activity_email(event, activity, justification)
    except SMTPException as error:
        logger.error(error)
        messages.error(request, _("The email couldn't sent successfully, \
                                  please retry later or contact a organizer"))
    safe_continue = reverse("activity_detail", args=[event_slug, activity.pk])
    return goto_next_or_continue(request.GET.get('next'), safe_continue)


@login_required
@user_passes_test(is_organizer, 'index')
def reject_activity(request, event_slug, activity_id):
    reject_form = RejectForm(request.POST)
    justification = ''
    if reject_form.is_valid():
        justification = request.POST.get('justification', '')
    return change_activity_status(request, event_slug, activity_id, 3, justification)


@login_required
@user_passes_test(is_organizer, 'index')
def resend_proposal(request, event_slug, activity_id):
    return change_activity_status(request, event_slug, activity_id, 1)


@user_passes_test(are_activities_public, 'index')
def activities(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    proposed_activities, accepted_activities, rejected_activities = [], [], []
    activities_instances = Activity.objects.filter(event=event, is_dummy=False)
    dummy_activities = Activity.objects.filter(event=event, is_dummy=True)
    speakers = {activity.owner for activity in activities_instances}
    emails = ','.join([speaker.user.email for speaker in speakers])

    for activity in list(activities_instances):
        activity.labels = activity.labels.split(',')
        if activity.status == '1':
            proposed_activities.append(activity)
        elif activity.status == '2':
            accepted_activities.append(activity)
        else:
            rejected_activities.append(activity)
    for activity in list(dummy_activities) + list(activities_instances):
        setattr(activity, 'form', ActivityForm(event_slug, instance=activity))
        setattr(activity, 'reject_form', RejectForm())
        setattr(activity, 'errors', [])
    return render(
        request, 'activities/activities_home.html',
        update_event_info(
            event_slug,
            {
                'emails': emails,
                'dummy_activities': dummy_activities,
                'proposed_activities': proposed_activities,
                'accepted_activities': accepted_activities,
                'rejected_activities': rejected_activities
            }
        )
    )

@login_required
@user_passes_test(is_organizer, 'index')
def activities_csv(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    activities_instances = Activity.objects.get_activities_report(event)
    header = {
        'title': _('Title'),
        'abstract': _('Abstract'),
        'long_description': _('Description'),
        'activity_type': _('Type'),
        'labels': _('Labels'),
        'level': _('Level'),
        'additional_info': _('Additional info'),
        'speakers_names': _('Speakers names'),
        'owner__user__username': _('Speaker username'),
        'owner__user__first_name': _('Speaker first name'),
        'owner__user__last_name': _('Speaker last name'),
        'owner__user__email': _('Speaker email'),
        'speaker_bio': _('Speaker bio')
    }
    return render_to_csv_response(activities_instances, field_header_map=header)


@login_required
@user_passes_test(is_speaker, 'index')
def my_proposals(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    proposed_activities, accepted_activities, rejected_activities = [], [], []
    activities_instances = Activity.objects.filter(event=event, owner__user=request.user)
    for activity in list(activities_instances):
        activity.labels = activity.labels.split(',')
        if activity.status == '1':
            proposed_activities.append(activity)
        elif activity.status == '2':
            accepted_activities.append(activity)
        else:
            rejected_activities.append(activity)
    return render(
        request, 'activities/my_proposals.html',
        update_event_info(
            event_slug,
            {
                'proposed_activities': proposed_activities,
                'accepted_activities': accepted_activities,
                'rejected_activities': rejected_activities
            }
        )
    )

# pylint: disable=too-many-locals
@login_required
@user_passes_test(is_organizer, 'index')
def talk_registration(request, event_slug, proposal_id):
    errors, error = [], False
    event = get_object_or_404(Event, event_slug=event_slug)
    proposal = get_object_or_404(Activity, pk=proposal_id)
    talk_form = ActivityForm(event_slug, request.POST)
    if request.POST:
        request_post = request.POST.copy()
        start_time = parse_time(request.POST.get('start_date', ''))
        end_time = parse_time(request.POST.get('end_date', ''))
        if isinstance(start_time, datetime.time) or isinstance(end_time, datetime.time):
            date_id = request.POST.get('date')
            event_date = get_object_or_404(EventDate, id=date_id)
            start_date = datetime.datetime.combine(event_date.date, start_time)
            end_date = datetime.datetime.combine(event_date.date, end_time)
            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)
            request_post.update({
                'start_date': start_date,
                'end_date': end_date,
                'event': event.id
            })
            talk_form = ActivityForm(event_slug, request_post)
            if talk_form.is_valid():
                room_available = Activity.room_available(
                    request=request, proposal=talk_form.instance,
                    event_slug=event_slug, event_date=event_date.date)
                if room_available:
                    try:
                        proposal.status = 2
                        proposal.start_date = start_date
                        proposal.end_date = end_date
                        room = get_object_or_404(Room, pk=request.POST.get('room'))
                        proposal.room = room
                        proposal.save()
                        utils_email.send_activity_email(event, proposal)
                        messages.success(request, _("The talk was registered successfully!"))
                        safe_continue = reverse(
                            "activity_detail", args=[event_slug, proposal.pk])
                        return goto_next_or_continue(request.GET.get('next'), safe_continue)
                    except SMTPException as error:
                        logger.error(error)
                        messages.error(request, _("The email couldn't sent successfully, \
                                                  please retry later or contact a organizer"))
                    except Exception as error_message:
                        logger.error(error_message)
                        proposal.status = 1
                        proposal.start_date = None
                        proposal.end_date = None
                        proposal.room = None
                        proposal.save()
                        messages.error(request, _("The talk couldn't be registered, \
                                                  please retry confirm the talk"))
    forms = [talk_form]
    errors = get_forms_errors(forms)
    error = True
    if errors:
        messages.error(request, _("The talk couldn't be registered (check form errors)"))
    proposal.labels = proposal.labels.split(',')
    render_dict = {
        'multipart': False, 'errors': errors,
        'form': talk_form, 'error': error,
        'user': request.user, 'activity': proposal
    }
    return render(request,
                  'activities/detail.html',
                  update_event_info(event_slug, render_dict))
# pylint: enable=too-many-locals


@login_required
@user_passes_test(is_organizer, 'index')
def confirm_schedule(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event.schedule_confirmed = True
    event.save()
    return schedule(request, event_slug)


def event_add_image(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    form = EventImageCroppingForm(request.POST or None, request.FILES, instance=event)
    if request.POST:
        if form.is_valid():
            # If a new file is being upload
            if request.FILES:
                # If clear home_image is clicked, delete the image
                if request.POST.get('image-clear') or request.FILES:
                    form.cleaned_data['image'] = None
                # Save the changes and redirect to upload a new one or crop the new one
                event = form.save()
                event.save()
                messages.success(request, _("Please crop or upload a new image."))
                return redirect(
                    reverse(
                        'event_add_image',
                        args=[event_slug]
                    )
                )
            form.save()
            messages.success(request, _(
                "The event has been updated successfully! We'll contact you at the provided email"))
            return redirect(
                reverse(
                    'index',
                    args=[event_slug]
                )
            )
        messages.error(request, _("The event couldn't be updated. \
                                  Please check the form for errors"))
    return render(
        request,
        'event/image-cropping.html',
        update_event_info(
            event_slug,
            {'form': form}
        )
    )


@is_activity_public()
def activity_detail(request, event_slug, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.labels = activity.labels.split(',')
    params = {
        'activity': activity,
        'form': ActivityForm(event_slug, instance=activity),
        'reject_form': RejectForm(),
        'errors': []
    }
    return render(
        request,
        'activities/detail.html',
        update_event_info(event_slug, params)
    )


def schedule(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    event_dates = event.eventdate_set.order_by('date')
    activities_count = Activity.objects \
        .filter(event=event) \
        .filter(room__isnull=False) \
        .filter(status='2') \
        .order_by('start_date') \
        .count()

    if not event.schedule_confirmed or activities_count <= 0:
        return render(
            request,
            'activities/schedule_not_confirmed.html',
            update_event_info(
                event_slug,
                {},
                event=event
            )
        )

    activities_dict = {}

    for event_date in event_dates:
        activities_dict[event_date.date.strftime("%Y%m%d")] = Activity.objects \
            .filter(event=event, start_date__date=event_date.date) \
            .filter(room__isnull=False) \
            .filter(status='2') \
            .order_by('start_date')

    rooms = Room.objects.filter(event=event)
    schedule_rooms = [room.get_schedule_info() for room in rooms]

    schedule_activities = {}
    for date, activities_for_date in activities_dict.items():
        if activities_for_date.count() > 0:
            schedule_activities[date] = json.dumps({
                'activities': [activity.get_schedule_info() for activity in activities_for_date],
                'min_time': activities_for_date.first().start_date.time().strftime("%H:%M"),
                'max_time': sorted(
                    activities_for_date, key=lambda o: o.end_date.time()
                    )[-1].end_date.time().strftime("%H:%M"),
                'date': activities_for_date.first().start_date.date().isoformat(),
                'datestring': date_format(
                    activities_for_date.first().start_date,
                    format='SHORT_DATE_FORMAT', use_l10n=True)
            })

    return render(
        request,
        'activities/schedule.html',
        update_event_info(
            event_slug,
            {
                'rooms': json.dumps(schedule_rooms),
                'activities': schedule_activities,
                'dates': sorted(schedule_activities.keys())
            },
            event=event
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def rooms_list(request, event_slug):
    event = get_object_or_404(Event, event_slug=event_slug)
    rooms = Room.objects.filter(event=event)
    return render(
        request,
        'rooms/list.html',
        update_event_info(
            event_slug,
            {'rooms': rooms}
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_or_edit_room(request, event_slug, room_id=None):
    event = get_object_or_404(Event, event_slug=event_slug)
    room_form = RoomForm(request.POST or None)
    is_edit = False
    room = None
    if room_id is not None:
        room = get_object_or_404(Room, event=event, id=room_id)
        room_form = RoomForm(request.POST or None, instance=room)
        is_edit = True
    forms = [room_form]
    errors = []
    if request.POST:
        if room_form.is_valid():
            try:
                room = room_form.save()
                room.event = event
                room.save()
                if is_edit:
                    messages.success(
                        request,
                        _("The Room has been edited successfully.")
                    )
                else:
                    messages.success(
                        request,
                        _("The Room has been added successfully.")
                    )
                return redirect(reverse(
                    'rooms_list',
                    args=[event_slug]
                ))
            except Exception as error_message:
                logger.error(error_message)
                if room is not None:
                    Room.delete(room)
        if is_edit:
            messages.error(
                request,
                _("The room couldn't be edited (check form errors)")
            )
        else:
            messages.error(
                request,
                _("The room couldn't be added (check form errors)")
            )
        errors = get_forms_errors(forms)
    return render(
        request,
        'rooms/add-or-edit-form.html',
        update_event_info(
            event_slug,
            {'is_edit': is_edit, 'room': room if room else None,
             'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def delete_room(request, event_slug, room_id):
    event = get_object_or_404(Event, event_slug=event_slug)
    room = get_object_or_404(Room, event=event, id=room_id)
    activities_instances = Activity.objects.filter(room=room)
    if activities_instances.exists():
        messages.error(
            request,
            _(
                "The room has assigned activities."
            )
        )
    else:
        room.delete()
        messages.success(
            request,
            _(
                "The Room has been removed successfully."
            )
        )
    return redirect(reverse(
        'rooms_list',
        args=[event_slug]
    ))


def generic_report(request):
    events_private_data = None
    user = request.user
    if user.is_authenticated() and user.is_superuser:
        events_private_data = Event.objects.get_event_private_data()
    return render(
        request, 'generic-report.html', {
            'events_private_data': events_private_data,
            'ws_propocol': settings.WS_PROTOCOL
        })


def activity_vote(request, event_slug, activity_id, vote_type):
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user
    activity.votes.delete(user.id)
    if vote_type == 'up':
        activity.votes.up(user.id)
    elif vote_type == 'down':
        activity.votes.down(user.id)
    safe_continue = reverse("activity_detail", args=[event_slug, activity.pk])
    return goto_next_or_continue(request.GET.get('next'), safe_continue)


@login_required
@user_passes_test(is_reviewer, 'index')
def activity_vote_up(request, event_slug, activity_id):
    return activity_vote(request, event_slug, activity_id, 'up')


@login_required
@user_passes_test(is_reviewer, 'index')
def activity_vote_down(request, event_slug, activity_id):
    return activity_vote(request, event_slug, activity_id, 'down')


@login_required
@user_passes_test(is_reviewer, 'index')
def activity_vote_cancel(request, event_slug, activity_id):
    return activity_vote(request, event_slug, activity_id, 'cancel')
