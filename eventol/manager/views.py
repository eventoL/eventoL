# encoding: UTF-8
import datetime
import io
import itertools
import json
import os
import uuid
import logging
import cairosvg
import pyqrcode
import svglue

from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import localize
from lxml import etree

from manager.forms import CollaboratorRegistrationForm, InstallationForm, \
    HardwareForm, InstallerRegistrationForm, EventDateModelFormset, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, \
    EventUserRegistrationForm, AttendeeRegistrationForm, \
    EventForm, ContactMessageForm, ImageCroppingForm, EventImageCroppingForm, \
    EventUserSearchForm, ContactForm, ActivityProposalForm, EventDateForm
from manager.models import Attendee, Organizer, EventUser, Room, Event, \
    Contact, Activity, Hardware, Installation, Collaborator, ContactMessage, \
    Installer, InstallationMessage, EventDate, \
    AttendeeAttendanceDate, EventUserAttendanceDate
from manager.security import is_installer, is_organizer, user_passes_test, \
    add_attendance_permission, is_collaborator, \
    add_organizer_permissions

from .utils import email


logger = logging.getLogger('eventol')


# Auxiliary functions
def update_event_info(event_slug, event_uid, request, render_dict=None, event=None):
    event = event or Event.objects.filter(slug__iexact=event_slug, uid=event_uid).get()
    if not event:
        return handler404(request)
    contacts = Contact.objects.filter(event=event)
    render_dict = render_dict or {}
    render_dict.update({
        'event_slug': event_slug,
        'event_uid': event_uid,
        'event': event,
        'contacts': contacts
    })
    return render_dict


def count_by(elements, getter, increment=None):
    return_dict = {}
    for element in elements:
        try:
            field = getter(element)
            if field in return_dict:
                return_dict[field] += increment(element) if increment else 1
            else:
                return_dict[field] = increment(element) if increment else 1
        except Exception as error:
            logger.error(error)
            pass
    return return_dict


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def generate_ticket(user):
    ticket_data = user.get_ticket_data()
    ticket_template = svglue.load(
        file=os.path.join(
            settings.STATIC_ROOT, 'manager/img/ticket_template_p.svg'))
    ticket_template.set_text(
        'event_name', "FLISoL " + ticket_data['event'].name[:24])
    ticket_template.set_text(
        'event_date', localize(ticket_data['event_date']))
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
    qr = pyqrcode.create(str(ticket_data['ticket']))
    code = io.BytesIO()
    qr.png(code, scale=7, quiet_zone=0)
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
    return etree.tostring(ticket_template._doc, encoding='utf8', method='xml')


def send_event_ticket(user):
    ticket_svg = generate_ticket(user)
    ticket_data = user.get_ticket_data()
    try:
        email.send_ticket_email(ticket_data, ticket_svg)
        ticket_data['ticket'].sent = True
        ticket_data['ticket'].save()
    except Exception as error:
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


# Views
def index(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    if event.external_url:
        return redirect(event.external_url)

    activities = Activity.objects.filter(event=event) \
        .exclude(image__isnull=True) \
        .exclude(is_dummy=True) \
        .distinct()

    dates = EventDate.objects.filter(event=event)

    render_dict = {'activities': activities, 'dates': dates}
    return render(
        request,
        'event/index.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            render_dict,
            event
        )
    )


def event_slug_index(request, event_slug):
    # Redirect to the most recent event, for now
    event = Event.objects.filter(slug__iexact=event_slug).order_by('-created_at').first()
    if not event:
        return handler404(request)
    return redirect(reverse('index', args=[event.slug, event.uid]))


def event_view(request, event_slug, event_uid, html='index.html'):
    return render(
        request,
        html,
        update_event_info(
            event_slug,
            event_uid,
            request
        )
    )


def home(request):
    if 'registration_event_uid' in request.session and request.user.is_authenticated():
        event_slug = request.session.pop('registration_event_slug')
        event_uid = request.session.pop('registration_event_uid')
        role = request.session.pop('registration_role')
        event_index = reverse(
            '{}_registration'.format(role),
            args=[event_slug, event_uid])
        return redirect(event_index)
    return render(request, 'index.html')


@login_required
@user_passes_test(is_installer, 'installer_registration')
def installation(request, event_slug, event_uid):
    installation_form = InstallationForm(
        request.POST or None, prefix='installation')
    hardware_form = HardwareForm(request.POST or None, prefix='hardware')
    forms = [installation_form, hardware_form]
    errors = []
    if request.POST:
        if hardware_form.is_valid() and installation_form.is_valid():
            try:
                hardware = hardware_form.save()
                install = installation_form.save()
                install.hardware = hardware
                event = Event.objects.filter(uid=event_uid).get()
                if not event:
                    return handler404(request)
                install.event = event
                install.installer = EventUser.objects \
                    .filter(user=request.user).filter(event=event).first()
                install.save()
                # Send post-install email if its defined
                postinstall_email = InstallationMessage.objects \
                    .filter(event=event).first()
                if postinstall_email:
                    try:
                        email.send_installation_email(
                            event.name, postinstall_email, install.attendee)
                    except Exception:
                        # Don't raise email exception to form exception
                        pass
                messages.success(
                    request,
                    _(
                        "The installation has been registered successfully. "
                        "Happy Hacking!"
                    )
                )
                event_index_url = reverse(
                    'index',
                    args=[event_slug, event_uid]
                )
                return redirect(event_index_url)
            except Exception as e:
                logger.error(e)
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
            event_uid,
            request,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def manage_attendance(request, event_slug, event_uid):
    attendee_form = AttendeeSearchForm(
        event_uid,
        request.POST or None
    )
    collaborator_form = EventUserSearchForm(
        event_uid,
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
                            args=[event_slug, event_uid]
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
                        args=[event_slug, event_uid]
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
            event_uid,
            request,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendance_by_ticket(request, event_slug, event_uid, ticket_code):
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
            args=[event_slug, event_uid]
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_organizer(request, event_slug, event_uid):
    form = EventUserSearchForm(event_uid, request.POST or None)
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
                    args=[event_slug, event_uid]
                )
            )

        messages.error(
            request,
            _(
                'Something went wrong (please check form errors)'
            )
        )

    organizers = Organizer.objects.filter(
        event_user__event__uid=event_uid
    )
    return render(
        request,
        'event/organizers.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': form, 'organizers': organizers}
        )
    )


@login_required
@user_passes_test(is_organizer, 'index')
def add_registration_people(request, event_slug, event_uid):
    form = EventUserSearchForm(event_uid, request.POST or None)
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
                    args=[event_slug, event_uid]
                )
            )

        messages.error(
            request,
            _(
                'Something went wrong (please check form errors)'
            )
        )

    content_type = ContentType.objects.get_for_model(Attendee)
    if Permission.objects.filter(codename='can_take_attendance', content_type=content_type).exists():
        permission = Permission.objects.get(
            codename='can_take_attendance',
            content_type=content_type
        )
        registration_people = Collaborator.objects.filter(
            event_user__user__user_permissions=permission,
            event_user__event__uid=event_uid
        )
    else:
        registration_people = []

    return render(
        request,
        'event/registration_people.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': form, 'registration_people': registration_people}
        )
    )


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_registration_by_collaborator(request, event_slug, event_uid):
    manage_attendance_url = reverse(
        'manage_attendance',
        args=[event_slug, event_uid]
    )
    event = Event.objects.filter(uid=event_uid).first()
    if not event:
        return handler404(request)
    form = AttendeeRegistrationByCollaboratorForm(
        request.POST or None,
        initial={'event': event}
    )
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Attendee.objects.filter(event=event, email__iexact=email).count() > 0:
                messages.error(
                    request,
                    _(
                        'The attendee is already registered for this event, '
                        'use correct form'
                    )
                )
                return redirect(manage_attendance_url)
            try:
                attendee = form.save()
                attendance_date = AttendeeAttendanceDate()
                attendance_date.attendee = attendee
                attendance_date.save()
                messages.success(
                    request,
                    _(
                        'The attendee was successfully registered. '
                        'Happy Hacking!'
                    )
                )
                return redirect(manage_attendance_url)
            except Exception as e:
                logger.error(e)
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
    return render(
        request,
        'registration/attendee/by-collaborator.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': form}
        )
    )


def contact(request, event_slug, event_uid):
    event = Event.objects.filter(uid=event_uid).get()
    if not event:
        return handler404(request)
    contact_message = ContactMessage()
    form = ContactMessageForm(request.POST or None, instance=contact_message)
    if request.POST:
        if form.is_valid():
            contact_message = form.save()
            info = _("Message received from ") + contact_message.name + "\n"
            info += _("User email: ") + contact_message.email + "\n"
            contact_message.message = info + contact_message.message

            email = EmailMessage()
            email.subject = _("eventoL Contact Message from " + contact_message.name)
            email.body = contact_message.message
            email.from_email = contact_message.email
            email.to = [event.email]
            email.extra_headers = {'Reply-To': contact_message.email}
            email.send(fail_silently=False)
            event = Event.objects.filter(uid=event_uid).get()
            if not event:
                return handler404(request)
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
                    args=[event_slug, event_uid]
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
            event_uid,
            request,
            {'form': form},
            event
        )
    )


def reports(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    event_dates = EventDate.objects.filter(event=event)
    confirmed_attendees_count, not_confirmed_attendees_count, speakers_count = 0, 0, 0

    installers = Installer.objects.filter(event_user__event=event)
    installations = Installation.objects.filter(attendee__event=event)
    talks = Activity.objects.filter(event=event).filter(is_dummy=False)
    collaborators = Collaborator.objects.filter(event_user__event=event)
    collaborators_event_users = [collaborator.event_user for collaborator in collaborators]
    installers_event_users = [installer.event_user for installer in installers]
    attendees = Attendee.objects.filter(event=event)

    attendees_attendance = AttendeeAttendanceDate.objects.filter(attendee__event=event).order_by('attendee').distinct()
    confirmed_attendees_count = attendees_attendance.count()
    not_confirmed_attendees_count = attendees.count() - confirmed_attendees_count

    confirmed_collaborators_count = EventUserAttendanceDate.objects.filter(event_user__event=event, event_user__in=collaborators_event_users).order_by('event_user').distinct().count()
    not_confirmed_collaborators_count = collaborators.count() - confirmed_collaborators_count
    confirmed_installers_count = EventUserAttendanceDate.objects.filter(event_user__event=event, event_user__in=installers_event_users).order_by('event_user').distinct().count()
    not_confirmed_installers_count = installers.count() - confirmed_installers_count

    speakers = []
    for talk in talks:
        speakers.append(talk.speakers_names.split(','))
    speakers_count = len(set(itertools.chain.from_iterable(speakers)))

    attendance_by_date = {}
    for event_date in event_dates:
        attendance_for_date = AttendeeAttendanceDate.objects.filter(attendee__event=event, date__date=event_date.date).order_by('attendee').distinct()
        attendance_by_date[event_date.date.strftime("%Y-%m-%d")] = count_by(attendance_for_date, lambda attendance: attendance.date.hour - 3)

    template_dict = {
        'event_dates': [event_date.date.strftime("%Y-%m-%d") for event_date in event_dates],
        'confirmed_attendees_count': confirmed_attendees_count,
        'not_confirmed_attendees_count': not_confirmed_attendees_count,
        'confirmed_collaborators_count': confirmed_collaborators_count,
        'not_confirmed_collaborators_count': not_confirmed_collaborators_count,
        'confirmed_installers_count': confirmed_installers_count,
        'not_confirmed_installers_count': not_confirmed_installers_count,
        'speakers_count': speakers_count,
        'organizers_count': Organizer.objects.filter(event_user__event=event).count(),
        'activities_count': talks.count(),
        'installations_count': Installation.objects.filter(attendee__event=event).count(),
        'installers_for_level': count_by(installers, lambda inst: inst.level),
        'installers_count': installers.count(),
        'installation_for_software': count_by(installations, lambda inst: inst.software.name),
        'registered_in_time': count_by(attendees, lambda attendee: attendee.registration_date.date()),
        'attendance_by_date': attendance_by_date
    }

    return render(
        request,
        'reports/dashboard.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            render_dict=template_dict
        )
    )

@login_required
def generic_registration(request, event_slug, event_uid, registration_model, new_role_form, msg_success, msg_error, template):
    event = get_object_or_404(Event, uid=event_uid)

    if not event.registration_is_open:
        return render(
            request,
            'registration/closed-registration.html',
            update_event_info(event_slug, event_uid, request)
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
        return redirect(reverse("index", args=[event_slug, event_uid]))

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

                #                if not event_user.ticket:
                #                    try:
                #                        send_event_ticket(event_user)
                #                        event_user.ticket = True
                #                        event_user.save()
                #                        msg_success += unicode(_(". Please check your email for the corresponding ticket."))
                #                    except Exception:
                #                        msg_success += unicode(
                # _(" but we couldn't send you your ticket. Please, check it out from the
                # menu."))
                messages.success(request, msg_success)
                return redirect(
                    reverse(
                        'index',
                        args=[event_slug, event_uid]
                    )
                )
            except Exception as e:
                logger.error(e)
                pass
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
            event_uid,
            request,
            {'forms': forms, 'errors': errors, 'multipart': False}
        )
    )


def get_email_confirmation_url(request, event_slug, event_uid, attendee_id, token):
    url = reverse(
        "attendee_confirm_email",
        args=[event_slug, event_uid, attendee_id, token])
    ret = build_absolute_uri(
        request,
        url)
    return ret


def attendee_registration(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)

    if not event.registration_is_open:
        return render(
            request,
            'registration/closed-registration.html',
            update_event_info(
                event_slug,
                event_uid,
                request,
                event=event
            )
        )

    attendee_form = AttendeeRegistrationForm(request.POST or None,
                                             initial={'event': event})
    if request.POST:
        if attendee_form.is_valid():
            try:
                attendee = attendee_form.save(commit=False)
                attendee.event = event
                attendee.registration_date = timezone.now()
                attendee.email_token = uuid.uuid4().hex
                attendee.save()

                body = _("Hi! You're receiving this message because you've registered to attend to " +
                         "FLISoL %(event_name)s.\n\nPlease follow this link to confirm your email address and we'll " +
                         "send you your ticket.\n\n%(confirm_url)s") % {'event_name': event.name,
                                                                         'confirm_url': get_email_confirmation_url(
                                                                             request,
                                                                             event_slug,
                                                                             event_uid,
                                                                             attendee.id,
                                                                             attendee.email_token)}

                email = EmailMessage()
                email.subject = _("[FLISoL] Please confirm your email")
                email.body = body
                email.from_email = settings.EMAIL_FROM
                email.to = [attendee.email]
                email.extra_headers = {'Reply-To': settings.EMAIL_FROM}
                email.send(fail_silently=False)
                return redirect(
                    reverse(
                        'attendee_email_sent',
                        args=[event_slug, event_uid]
                    )
                )
            except Exception as e:
                logger.error(e)
                if attendee is not None:
                    attendee.delete()

        messages.error(request, _("There is a problem with the registration (check form errors)"))

    return render(
        request,
        'registration/attendee-registration.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {
                'form': attendee_form,
                'errors': get_forms_errors([attendee_form]),
                'multipart': False
            },
            event=event
        )
    )


def attendee_confirm_email(request, event_slug, event_uid, pk, token):
    attendee = Attendee.objects.get(pk=pk)
    title = _("Email verification")
    message = _(
        "We've sent you your ticket to your email! In case it doesn't arrive, don't worry! You're already registered and we'll ask for your email address.")
    if not attendee.email_confirmed:
        if attendee.email_token == token:
            try:
                attendee.email_confirmed = True
                attendee.save()
                send_event_ticket(attendee)
            except Exception as e:
                logger.error(e)
                pass
        else:
            message = _("The verification URL is invalid. Try again. ")

    return render(
        request,
        'registration/attendee/ticket-sent.html',
        {
            'message': message,
            'title': title,
            'event_slug': event_slug,
            'event_uid': event_uid
        }
    )


def installer_registration(request, event_slug, event_uid):
    if not request.user.is_authenticated():
        request.session['registration_event_uid'] = event_uid
        request.session['registration_event_slug'] = event_slug
        request.session['registration_role'] = 'installer'
    msg_success = _("You have successfully registered as an installer")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/installer-registration.html'
    return generic_registration(
        request,
        event_slug,
        event_uid,
        Installer,
        InstallerRegistrationForm,
        msg_success,
        msg_error,
        template
    )


def collaborator_registration(request, event_slug, event_uid):
    if not request.user.is_authenticated():
        request.session['registration_event_uid'] = event_uid
        request.session['registration_event_slug'] = event_slug
        request.session['registration_role'] = 'collaborator'
    msg_success = _("You have successfully registered as a collaborator")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/collaborator-registration.html'
    return generic_registration(
        request,
        event_slug,
        event_uid,
        Collaborator,
        CollaboratorRegistrationForm,
        msg_success,
        msg_error,
        template
    )


@login_required
def create_event(request):
    event_form = EventForm(request.POST or None, prefix='event')
    ContactsFormSet = modelformset_factory(Contact, form=ContactForm, can_delete=True)

    contacts_formset = ContactsFormSet(request.POST or None, prefix='contacts-form', queryset=Contact.objects.none())

    EventDateFormset = modelformset_factory(EventDate, form=EventDateForm, formset=EventDateModelFormset,
                                            can_delete=True)
    event_date_formset = EventDateFormset(request.POST or None, prefix='event-date-form',
                                          queryset=EventDate.objects.none())

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid() and event_date_formset.is_valid():
            # Check if the slug is used then verify that this user is an organizer
            # issue 297
            event_slug = request.POST.get('event-slug')
            existing_event = Event.objects.filter(slug__iexact=event_slug).first() if event_slug else None
            if existing_event and not is_organizer(request.user, event_slug, existing_event.uid):
                event_form.add_error('slug', _('You are not an organizer for this event URL, use a different URL'))
            else:
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

                    return redirect(
                        reverse(
                            'event_add_image',
                            args=(the_event.slug, the_event.uid)
                        )
                    )
                except Exception as e:
                    logger.error(e)
                    try:
                        if organizer is not None:
                            Organizer.delete(organizer)
                        if event_user is not None:
                            EventUser.delete(event_user)
                        if the_event is not None:
                            Event.delete(the_event)
                        if contacts is not None:
                            for a_contact in contacts:
                                Contact.objects.delete(a_contact)
                        if event_dates is not None:
                            for event_date in event_dates:
                                EventDate.objects.delete(event_date)
                    except Exception:
                        pass

        messages.error(request, _("There is a problem with your event. Please check the form for errors."))
    return render(request,
                  'event/create.html', {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                        'contacts_formset': contacts_formset, 'event_date_formset': event_date_formset})


@login_required
@user_passes_test(is_organizer, 'index')
def edit_event(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    event_form = EventForm(request.POST or None, prefix='event', instance=event)
    ContactsFormSet = modelformset_factory(Contact, form=ContactForm, can_delete=True)

    contacts_formset = ContactsFormSet(request.POST or None, prefix='contacts-form', queryset=event.contacts.all())

    EventDateFormset = modelformset_factory(EventDate, form=EventDateForm, formset=EventDateModelFormset,
                                            can_delete=True)
    event_date_formset = EventDateFormset(request.POST or None, prefix='event-date-form',
                                          queryset=EventDate.objects.filter(event=event))

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

                return redirect(
                    reverse(
                        'index',
                        args=(the_event.slug, the_event.uid)
                    )
                )
            except Exception as e:
                logger.error(e)
                pass

        messages.error(request, _("There is a problem with your event. Please check the form for errors."))
    return render(
        request,
        'event/create.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {
                'form': event_form,
                'domain': request.get_host(),
                'protocol': request.scheme,
                'contacts_formset': contacts_formset,
                'event_date_formset': event_date_formset
            }
        )
    )


@login_required
def view_ticket(request, event_slug, event_uid):
    event_user = EventUser.objects.filter(event__uid=event_uid).filter(user=request.user).first()
    if event_user:
        ticket = generate_ticket(event_user)
        response = HttpResponse(cairosvg.svg2pdf(bytestring=ticket), content_type='application/pdf')
        response["Content-Disposition"] = 'filename=Ticket-' + str(ticket) + '.pdf'
        return response
    else:
        messages.error(request, "You are not registered for this event")
        return redirect(reverse("index", args=[event_slug, event_uid]))


@login_required
@user_passes_test(is_organizer, 'index')
def draw(request, event_slug, event_uid):
    users = [
        str(attendance_date.attendee) for attendance_date in
        AttendeeAttendanceDate.objects.filter(
            attendee__event__uid=event_uid,
            date__date=datetime.date.today()
        )
    ]
    return render(
        request,
        'event/draw.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'eventusers': users, 'eventusersjson': json.dumps(users)}
        )
    )


def activity_proposal(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)

    if not event.activity_proposal_is_open:
        messages.error(request,
                       _(
                           "The activity proposal is already closed or the event is not accepting proposals through this " +
                           "page. Please contact the Event Organization Team to submit it."))
        return redirect(reverse('index', args=[event_slug, event_uid]))

    activity = Activity(event=event, status='1')
    activity_form = ActivityProposalForm(request.POST or None, request.FILES or None, instance=activity)

    if request.POST:
        if activity_form.is_valid():
            try:
                activity = activity_form.save()
                return redirect(
                    reverse(
                        'image_cropping',
                        args=[event_slug, event_uid, activity.pk]
                    )
                )
            except Exception as e:
                logger.error(e)
                pass

        messages.error(request, _("There was a problem submitting the proposal. Please check the form for errors."))

    return render(
        request,
        'activities/proposal.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': activity_form, 'errors': [], 'multipart': True},
            event=event
        )
    )


def image_cropping(request, event_slug, event_uid, activity_id):
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
                        args=[event_slug, event_uid, activity.pk]
                    )
                )
            form.save()
            messages.success(request, _(
                "The proposal has been registered successfully! We'll contact you at the provided email"))
            return redirect(
                reverse(
                    'activity_detail',
                    args=[event_slug, event_uid, activity.pk]
                )
            )
        messages.error(request, _("The proposal couldn't be registered. Please check the form for errors"))
    return render(
        request,
        'activities/image-cropping.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': form}
        )
    )


def event_add_image(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
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
                        args=[event_slug, event_uid]
                    )
                )
            form.save()
            messages.success(request, _(
                "The event has been updated successfully! We'll contact you at the provided email"))
            return redirect(
                reverse(
                    'index',
                    args=[event_slug, event_uid]
                )
            )
        messages.error(request, _("The event couldn't be updated. Please check the form for errors"))
    return render(
        request,
        'event/image-cropping.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'form': form}
        )
    )


def activity_detail(request, event_slug, event_uid, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.labels = activity.labels.split(', ')
    return render(
        request,
        'activities/detail.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {'activity': activity}
        )
    )


def schedule(request, event_slug, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
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
                event_uid,
                request,
                {},
                event=event
            )
        )

    activities = {}

    for event_date in event_dates:
        activities[event_date.date.strftime("%Y%m%d")] = Activity.objects \
            .filter(event=event, start_date__date=event_date.date) \
            .filter(room__isnull=False) \
            .filter(status='2') \
            .order_by('start_date')

    rooms = Room.objects.filter(event=event)
    schedule_rooms = [room.get_schedule_info() for room in rooms]

    schedule_activities = {}
    for date, activities_for_date in activities.items():
        if activities_for_date.count() > 0:
            schedule_activities[date] = json.dumps({
                'activities': [activity.get_schedule_info() for activity in activities_for_date],
                'min_time': activities_for_date.first().start_date.time().strftime("%H:%M"),
                'max_time': sorted(activities_for_date, key=lambda o: o.end_date.time())[-1].end_date.time().strftime(
                    "%H:%M"),
                'date': activities_for_date.first().start_date.date().isoformat()
            })

    return render(
        request,
        'activities/schedule.html',
        update_event_info(
            event_slug,
            event_uid,
            request,
            {
                'rooms': json.dumps(schedule_rooms),
                'activities': schedule_activities,
                'dates': sorted(schedule_activities.keys())
            },
            event=event
        )
    )


def handler404(request):
    response = render_to_response(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(request, '500.html', {})
    response.status_code = 500
    return response
