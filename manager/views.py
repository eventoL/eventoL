# encoding: UTF-8
import datetime
import io
import itertools
import json
import os
import uuid

import cairosvg
import pyqrcode
import svglue
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import localize

from manager.forms import CollaboratorRegistrationForm, InstallationForm, HardwareForm, InstallerRegistrationForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, \
    EventUserRegistrationForm, AttendeeRegistrationForm, \
    EventForm, ContactMessageForm, ImageCroppingForm, \
    EventUserSearchForm, ContactForm, ActivityProposalForm, EventDateForm, EventDateModelFormset
from manager.models import Attendee, Organizer, EventUser, Room, Event, Contact, \
    Activity, Hardware, Installation, Collaborator, ContactMessage, Installer, \
    InstallationMessage, EventDate, AttendeeAttendanceDate, EventUserAttendanceDate
from manager.security import is_installer, is_organizer, user_passes_test, add_attendance_permission, is_collaborator, \
    add_organizer_permissions


# Auxiliary functions
def update_event_info(event_slug, request, render_dict=None, event=None):
    event = event or Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    contacts = Contact.objects.filter(event=event)
    render_dict = render_dict or {}
    render_dict.update({
        'event_slug': event_slug,
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
        except Exception:
            pass
    return return_dict


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def generate_ticket(user):
    ticket_data = user.get_ticket_data()
    ticket_template = svglue.load(file=os.path.join(settings.STATIC_ROOT, 'manager/img/ticket_template_p.svg'))
    ticket_template.set_text('event_name', ticket_data['event'].name[:30])
    ticket_template.set_text('event_date', localize(ticket_data['event_date']).decode('utf-8'))
    place = json.loads(ticket_data['event'].place)
    if place.get("name"):  # Si tiene nombre cargado
        ticket_template.set_text('event_place_name', place.get("name"))
        ticket_template.set_text('event_place_address', place.get("formatted_address")[:50])
    else:
        ticket_template.set_text('event_place_name', place.get("formatted_address")[:50])
        ticket_template.set_text('event_place_address', '')

    ticket_template.set_text('ticket_type', unicode(_(u"General Ticket")))
    qr = pyqrcode.create(ticket_data['ticket'].id)
    code = io.BytesIO()
    qr.png(code, scale=7, quiet_zone=0)
    ticket_template.set_image('qr_code', code.getvalue(), mimetype='image/png')
    ticket_template.set_text('eventUser_PK', str(ticket_data['ticket'].id).zfill(12))
    ticket_template.set_text('eventUser_email', ticket_data['email'])

    if ticket_data['first_name'] is not None or ticket_data['last_name'] is not None:
        user_name_l1 = u"%s %s" % (ticket_data['first_name'], ticket_data['last_name'])
        user_name_l2 = ''
        if len(user_name_l1) > 30:
            user_name_l1 = ticket_data['first_name'][:30]  # Por si tiene mas de 30 caracteres
            user_name_l2 = ticket_data['last_name'][:30]
    elif ticket_data.nickname is not None:
        user_name_l1 = u"%s" % ticket_data['nickname'][:30]
        user_name_l2 = ''
    elif ticket_data['email'] is not None:
        user_name_l1 = u"%s" % ticket_data['email'][:30]
        user_name_l2 = ''

    ticket_template.set_text('eventUser_name_l1', user_name_l1)
    ticket_template.set_text('eventUser_name_l2', user_name_l2)

    return str(ticket_template)


def send_event_ticket(user):
    ticket_svg = generate_ticket(user)
    ticket_data = user.get_ticket_data()

    try:
        email = EmailMessage()
        subject = _(u"Ticket for %(event_name)s event") % {'event_name': ticket_data['event'].name}
        body = _(u"Hello %(first_name)s %(last_name)s,\nHere is your ticket for %(event_name)s event." +
                 u" Please remember to print it and bring it with you the day of the event.\n" +
                 u"Regards, FLISoL %(event_name)s team.") % {'event_name': ticket_data['event'].name,
                                                             'first_name': ticket_data['first_name'],
                                                             'last_name': ticket_data['last_name']}
        email.subject = unicode(subject)
        email.body = unicode(body)
        email.to = [ticket_data['email']]
        email.attach('Ticket-' + str(ticket_data['ticket'].id).zfill(12) + '.pdf',
                     cairosvg.svg2pdf(bytestring=ticket_svg),
                     'application/pdf')
        email.send(fail_silently=False)
        ticket_data['ticket'].sent = True
        ticket_data['ticket'].save()
    except Exception as e:
        ticket_data['ticket'].sent = False
        ticket_data['ticket'].save()
        raise e


def create_organizer(event_user):
    organizer = Organizer.objects.filter(event_user=event_user).first()
    if organizer is None:
        organizer = Organizer.objects.create(event_user=event_user)

    add_organizer_permissions(organizer.event_user.user)
    organizer.save()
    return organizer


# Views


def index(request, event_slug):
    event = get_object_or_404(Event, slug__iexact=event_slug)
    if event.external_url:
        return HttpResponseRedirect(event.external_url)

    activities = Activity.objects.filter(event=event) \
        .exclude(image__isnull=True) \
        .distinct()

    dates = EventDate.objects.filter(event=event)

    render_dict = {'activities': activities, 'dates': dates}
    return render(request, 'event/index.html', update_event_info(event_slug, request, render_dict, event))


def event_view(request, event_slug, html='index.html'):
    return render(request, html, update_event_info(event_slug, request))


def home(request):
    events = Event.objects.all()
    return render(request, 'homepage.html', {'events': events})


@login_required
@user_passes_test(is_installer, 'installer_registration')
def installation(request, event_slug):
    installation_form = InstallationForm(request.POST or None, prefix='installation')
    hardware_form = HardwareForm(request.POST or None, prefix='hardware')
    forms = [installation_form, hardware_form]
    errors = []
    if request.POST:
        if hardware_form.is_valid() and installation_form.is_valid():
            try:
                hardware = hardware_form.save()
                install = installation_form.save()
                install.hardware = hardware
                event = Event.objects.filter(slug__iexact=event_slug).first()
                if not event:
                    return handler404(request)
                install.event = event
                install.installer = EventUser.objects.filter(user=request.user).filter(event=event).first()
                install.save()
                # Send post-install email if its defined
                postinstall_email = InstallationMessage.objects.filter(event=event).first()
                if postinstall_email:
                    attendee = install.attendee
                    email = EmailMultiAlternatives()
                    subject = _(
                        u"%(first_name)s %(last_name)s, thank you for participating in FLISoL %(event_name)s") % {
                                  'event_name': event.name, 'first_name': attendee.first_name,
                                  'last_name': attendee.last_name}
                    email.from_email = postinstall_email.contact_email
                    email.subject = unicode(subject)
                    email.body = ''
                    email.attach_alternative(postinstall_email.message, "text/html")
                    email.to = [attendee.email]
                    try:
                        email.send(fail_silently=False)
                    except Exception:
                        # Don't raise email exception to form exception
                        pass
                messages.success(request, _("The installation has been registered successfully. Happy Hacking!"))
                return HttpResponseRedirect('/event/' + event_slug)
            except Exception:
                if hardware is not None:
                    Hardware.delete(hardware)
                if install is not None:
                    Installation.delete(install)
        messages.error(request, _("The installation couldn't be registered (check form errors)"))
        errors = get_forms_errors(forms)

    return render(request,
                  'installation/installation-form.html',
                  update_event_info(event_slug, request, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def manage_attendance(request, event_slug):
    attendee_form = AttendeeSearchForm(event_slug, request.POST or None)
    collaborator_form = EventUserSearchForm(event_slug, request.POST or None)
    forms = [attendee_form, collaborator_form]
    errors = []
    if request.POST:
        if attendee_form.is_valid():
            attendee = attendee_form.cleaned_data['attendee']
            if attendee:
                if attendee.attended_today():
                    messages.success(request, _('The attendee has already been registered correctly.'))
                else:
                    attendance_date = AttendeeAttendanceDate()
                    attendance_date.attendee = attendee
                    attendance_date.save()
                    messages.success(request, _('The attendee has been successfully registered. Happy Hacking!'))
                return HttpResponseRedirect(reverse("manage_attendance", args=[event_slug]))
        if collaborator_form.is_valid():
            event_user = collaborator_form.cleaned_data['event_user']
            if event_user:
                if event_user.attended_today():
                    messages.success(request, _('The collaborator has already been registered correctly.'))
                else:
                    attendance_date = EventUserAttendanceDate()
                    attendance_date.event_user = event_user
                    attendance_date.save()
                    messages.success(request, _('The collaborator has been successfully registered. Happy Hacking!'))
                return HttpResponseRedirect(reverse("manage_attendance", args=[event_slug]))

        messages.error(request, _("There was a problem registering the attendee. Please try again."))

        errors = get_forms_errors(forms)

    return render(request,
                  'registration/attendee/search.html',
                  update_event_info(event_slug, request, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendance_by_ticket(request, event_slug, pk):
    attendee = Attendee.objects.filter(ticket__pk=pk).first()
    if not attendee:
        attendee = EventUser.objects.filter(ticket__pk=pk).first()

    if attendee:
        if attendee.attended_today():
            messages.success(request, _('The attendee has already been registered correctly.'))
        else:
            if hasattr(attendee, 'user'):
                attendance_date = EventUserAttendanceDate()
                attendance_date.event_user = attendee
            else:
                attendance_date = AttendeeAttendanceDate()
                attendance_date.attendee = attendee
            attendance_date.save()
            messages.success(request, _('The attendee has been successfully registered. Happy Hacking!'))
        return HttpResponseRedirect(reverse("manage_attendance", args=[event_slug]))

    messages.error(request, _("The user isn't registered for this event."))

    return HttpResponseRedirect(reverse("manage_attendance", args=[event_slug]))


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
                    _("%s has been successfully added as an Organizer." % organizer.event_user.user.username))
            return HttpResponseRedirect(reverse("add_organizer", args=[event_slug]))

        messages.error(request, _("Something went wrong (please check form errors)"))

    organizers = Organizer.objects.filter(event_user__event__slug__iexact=event_slug)
    return render(request, 'event/organizers.html',
                  update_event_info(event_slug, request, {'form': form, 'organizers': organizers}))


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
                messages.success(request,
                                 _("%s has been successfully added to manage attendance." % event_user.user.username))
            return HttpResponseRedirect(reverse("add_registration_people", args=[event_slug]))

        messages.error(request, _("Something went wrong (please check form errors)"))

    if Permission.objects.filter(codename='can_take_attendance').exists():
        permission = Permission.objects.get(codename='can_take_attendance')
        registration_people = Collaborator.objects.filter(event_user__user__user_permissions=permission,
                                                          event_user__event__slug__iexact=event_slug)
    else:
        registration_people = []

    return render(request, 'event/registration_people.html',
                  update_event_info(event_slug, request, {'form': form, 'registration_people': registration_people}))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_registration_by_collaborator(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None, initial={'event': event})
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Attendee.objects.filter(event=event, email__iexact=email).count() > 0:
                messages.error(request, _("The attendee is already registered for this event, use correct form"))
                return HttpResponseRedirect(reverse("manage_attendance", args=(event_slug,)))
            try:
                attendee = form.save()
                attendance_date = AttendeeAttendanceDate()
                attendance_date.attendee = attendee
                attendance_date.save()
                messages.success(request, _('The attendee was successfully registered . Happy Hacking!'))
                return HttpResponseRedirect(reverse("manage_attendance", args=(event_slug,)))
            except Exception:
                try:
                    if attendee is not None:
                        Attendee.objects.delete(attendee)
                    if attendance_date is not None:
                        AttendeeAttendanceDate.objects.delete(attendance_date)
                except Exception:
                    pass
        messages.error(request, _("The attendee couldn't be registered (check form errors)"))
    return render(request, 'registration/attendee/by-collaborator.html',
                  update_event_info(event_slug, request, {'form': form}))


def contact(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
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
            event = Event.objects.filter(slug__iexact=event_slug).first()
            if not event:
                return handler404(request)
            contact_message.event = event
            contact_message.save()
            messages.success(request, _("The message has been sent. You will receive a reply by email"))
            return HttpResponseRedirect('/event/' + event_slug)
        messages.error(request, _("There was a problem sending your message. Please try again in a few minutes."))

    return render(request, 'contact-message.html', update_event_info(event_slug, request, {'form': form}, event))


def reports(request, event_slug):
    # event = get_object_or_404(Event, slug__iexact=event_slug)
    # confirmed_attendees_count, not_confirmed_attendees_count, speakers_count = 0, 0, 0
    #
    # installers = Installer.objects.filter(event_user__event=event)
    # installations = Installation.objects.filter(attendee__event=event)
    # talks = Activity.objects.filter(event=event).filter(is_dummy=False)
    # collaborators = Collaborator.objects.filter(event_user__event=event)
    # attendees = Attendee.objects.filter(event=event)
    #
    # confirmed_attendees_count = Attendee.objects.filter(event=event).filter(attended=True).count()
    #
    # not_confirmed_attendees_count = Attendee.objects.filter(event=event).filter(attended=False).count()
    #
    # for talk in talks:
    #     speakers_count += len(talk.speakers_names.split(','))
    #
    # template_dict = {
    #     'confirmed_attendees_count': confirmed_attendees_count,
    #     'not_confirmed_attendees_count': not_confirmed_attendees_count,
    #     'confirmed_collaborators_count': collaborators.filter(event_user__attended=True).count(),
    #     'not_confirmed_collaborators_count': collaborators.filter(event_user__attended=False).count(),
    #     'confirmed_installers_count': installers.filter(event_user__attended=True).count(),
    #     'not_confirmed_installers_count': installers.filter(event_user__attended=False).count(),
    #     'speakers_count': speakers_count,
    #     'organizers_count': Organizer.objects.filter(event_user__event=event).count(),
    #     'activities_count': talks.count(),
    #     'installations_count': Installation.objects.filter(attendee__event=event).count(),
    #     'installers_for_level': count_by(installers, lambda inst: inst.level),
    #     'installers_count': installers.count(),
    #     'installation_for_software': count_by(installations, lambda inst: inst.software.name),
    #     'registered_in_time': count_by(attendees, lambda attendee: attendee.registration_date.date())
    # }

    template_dict = {}
    return render(request, 'reports/dashboard.html', update_event_info(event_slug, request, render_dict=template_dict))


@login_required
def generic_registration(request, event_slug, registration_model, new_role_form, msg_success, msg_error, template):
    event = get_object_or_404(Event, slug__iexact=event_slug)

    if not event.registration_is_open:
        return render(request, 'registration/closed-registration.html', update_event_info(event_slug, request))

    errors = []
    event_user = EventUser.objects.filter(event=event, user=request.user).first()
    if not event_user:
        event_user = EventUser(event=event, user=request.user)

    new_role = registration_model.objects.filter(event_user=event_user)

    if new_role:
        # Ya esta registrado con ese "rol"
        messages.error(request, _("You are already registered for this event"))
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))

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
                return HttpResponseRedirect('/event/' + event_slug)
            except Exception:
                pass
        messages.error(request, msg_error)
    else:
        event_user_form = EventUserRegistrationForm(instance=event_user)
        new_role_form = new_role_form(instance=new_role)
        forms = [event_user_form, new_role_form]

    return render(request,
                  template,
                  update_event_info(event_slug, request, {'forms': forms, 'errors': errors, 'multipart': False}))


def get_email_confirmation_url(request, event_slug, attendee_id, token):
    url = reverse(
        "attendee_confirm_email",
        args=[event_slug, attendee_id, token])
    ret = build_absolute_uri(
        request,
        url)
    return ret


def attendee_registration(request, event_slug):
    event = get_object_or_404(Event, slug__iexact=event_slug)

    if not event.registration_is_open:
        return render(request, 'registration/closed-registration.html',
                      update_event_info(event_slug, request, event=event))

    attendee_form = AttendeeRegistrationForm(request.POST or None,
                                             initial={'event': event})
    if request.POST:
        if attendee_form.is_valid():
            try:
                attendee = attendee_form.save(commit=False)
                attendee.event = event
                attendee.registration_date = datetime.datetime.now()
                attendee.email_token = uuid.uuid4().hex
                attendee.save()

                body = _(u"Hi! You're receiving this message because you've registered to attend to " +
                         u"FLISoL %(event_name)s.\n\nPlease follow this link to confirm your email address and we'll " +
                         u"send you your ticket.\n\n%(confirm_url)s") % {'event_name': event.name,
                                                                         'confirm_url': get_email_confirmation_url(
                                                                             request,
                                                                             event_slug,
                                                                             attendee.id,
                                                                             attendee.email_token)}

                email = EmailMessage()
                email.subject = unicode(_(u"[FLISoL] Please confirm your email"))
                email.body = unicode(body)
                email.from_email = settings.EMAIL_FROM
                email.to = [attendee.email]
                email.extra_headers = {'Reply-To': settings.EMAIL_FROM}
                email.send(fail_silently=False)
                return HttpResponseRedirect(reverse("attendee_email_sent", args=[event_slug]))
            except Exception:
                if attendee is not None:
                    attendee.delete()
        messages.error(request, _("There is a problem with the registration (check form errors)"))

    return render(request, 'registration/attendee-registration.html', update_event_info(event_slug, request,
                                                                                        {'form': attendee_form,
                                                                                         'errors': get_forms_errors(
                                                                                             [attendee_form]),
                                                                                         'multipart': False},
                                                                                        event=event))


def attendee_confirm_email(request, event_slug, pk, token):
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
            except Exception:
                pass
        else:
            message = _("The verification URL is invalid. Try again. ")

    return render(request, 'registration/attendee/ticket-sent.html',
                  {'message': message, 'title': title, 'event_slug': event_slug})


@login_required
def installer_registration(request, event_slug):
    msg_success = _("You have successfully registered as an installer")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/installer-registration.html'
    return generic_registration(request, event_slug, Installer,
                                InstallerRegistrationForm, msg_success, msg_error, template)


@login_required
def collaborator_registration(request, event_slug):
    msg_success = _("You have successfully registered as a collaborator")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/collaborator-registration.html'
    return generic_registration(request, event_slug, Collaborator,
                                CollaboratorRegistrationForm, msg_success, msg_error, template)


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

                return HttpResponseRedirect(reverse("index", args=(the_event.slug,)))
            except Exception:
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
def edit_event(request, event_slug):
    event = get_object_or_404(Event, slug__iexact=event_slug)
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

                return HttpResponseRedirect(reverse("index", args=(the_event.slug,)))
            except Exception:
                pass

        messages.error(request, _("There is a problem with your event. Please check the form for errors."))
    return render(request,
                  'event/create.html',
                  update_event_info(event_slug, request,
                                    {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                     'contacts_formset': contacts_formset, 'event_date_formset': event_date_formset}))


@login_required
def view_ticket(request, event_slug):
    event_user = EventUser.objects.filter(event__slug__iexact=event_slug).filter(user=request.user).first()
    if event_user:
        ticket = generate_ticket(event_user)
        response = HttpResponse(cairosvg.svg2pdf(bytestring=ticket), content_type='application/pdf')
        response["Content-Disposition"] = 'filename=Ticket-' + str(event_user.id).zfill(12) + '.pdf'
        return response
    else:
        messages.error(request, "You are not registered for this event")
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))


@login_required
@user_passes_test(is_organizer, 'index')
def draw(request, event_slug):
    users = [unicode(attendance_date.attendee) for attendance_date in
             AttendeeAttendanceDate.objects.filter(attendee__event__slug__iexact=event_slug,
                                                   date__date=datetime.date.today())]
    return render(request, 'event/draw.html',
                  update_event_info(event_slug, request, {'eventusers': users, 'eventusersjson': json.dumps(users)}))


def activity_proposal(request, event_slug):
    event = get_object_or_404(Event, slug__iexact=event_slug)

    if not event.activity_proposal_is_open:
        messages.error(request,
                       _(
                           "The activity proposal is already closed or the event is not accepting proposals through this " +
                           "page. Please contact the Event Organization Team to submit it."))
        return HttpResponseRedirect(reverse('index', args=(event_slug,)))

    activity = Activity(event=event, status='1')
    activity_form = ActivityProposalForm(request.POST or None, request.FILES or None, instance=activity)

    if request.POST:
        if activity_form.is_valid():
            try:
                activity = activity_form.save()
                return HttpResponseRedirect(reverse('image_cropping', args=(event_slug, activity.pk)))
            except Exception:
                pass

        messages.error(request, _("There was a problem submitting the proposal. Please check the form for errors."))

    return render(request, 'activities/proposal.html',
                  update_event_info(event_slug, request, {'form': activity_form, 'errors': [], 'multipart': True},
                                    event=event))


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
                return HttpResponseRedirect(reverse('image_cropping', args=(event_slug, activity.pk)))
            form.save()
            messages.success(request, _(
                "The proposal has been registered successfully! We'll contact you at the provided email"))
            return HttpResponseRedirect(reverse('activity_detail', args=(event_slug, activity.pk)))
        messages.error(request, _("The proposal couldn't be registered. Please check the form for errors"))
    return render(request, 'activities/image-cropping.html',
                  update_event_info(event_slug, request, {'form': form}))


def activity_detail(request, event_slug, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.labels = activity.labels.split(', ')
    return render(request, 'activities/detail.html',
                  update_event_info(event_slug, request, {'activity': activity}, ))


def schedule(request, event_slug):
    event = get_object_or_404(Event, slug__iexact=event_slug)
    event_dates = event.eventdate_set.order_by('date')
    activities_count = Activity.objects \
        .filter(event=event) \
        .filter(room__isnull=False) \
        .filter(status='2') \
        .order_by('start_date') \
        .count()

    if not event.schedule_confirmed or activities_count <= 0:
        return render(request, 'activities/schedule_not_confirmed.html',
                      update_event_info(event_slug, request, {}, event=event))

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
                'max_time': activities_for_date.last().end_date.time().strftime("%H:%M"),
                'date': activities_for_date.first().start_date.date().isoformat()
            })

    return render(request, 'activities/schedule.html',
                  update_event_info(event_slug, request, {
                      'rooms': json.dumps(schedule_rooms),
                      'activities': schedule_activities,
                      'dates': sorted(schedule_activities.keys())
                  }, event=event))


def handler404(request):
    response = render_to_response(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(request, '500.html', {})
    response.status_code = 500
    return response
