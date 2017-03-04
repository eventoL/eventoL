# encoding: UTF-8
import datetime
import io
import itertools
import json
import uuid

from allauth.utils import build_absolute_uri
from autocomplete_light import shortcuts as autocomplete_light
import cairosvg
import locale
import os
import pyqrcode
import svglue
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils.translation import ugettext_lazy as _
from manager.forms import CollaboratorRegistrationForm, InstallationForm, HardwareForm, InstallerRegistrationForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, CommentForm, PresentationForm, \
    EventUserRegistrationForm, AttendeeRegistrationForm, ActivityForm, TalkForm, RoomForm, \
    EventForm, ContactMessageForm, TalkProposalForm, ImageCroppingForm, \
    RegisteredEventUserSearchForm, ActivityCompleteForm, ContactForm
from manager.models import Attendee, Organizer, EventUser, Room, Event, Contact, TalkProposal, \
    Activity, Hardware, Installation, Comment, Collaborator, ContactMessage, Installer, Speaker, \
    InstallationMessage
from manager.schedule import Schedule
from manager.security import is_installer, is_organizer, user_passes_test, add_attendance_permission, is_collaborator, \
    add_organizer_permissions
from voting.models import Vote

autocomplete_light.autodiscover()


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


def generate_ticket(user, lang='en_US.UTF8'):
    ticket_data = user.get_ticket_data()
    ticket_template = svglue.load(file=os.path.join(settings.STATIC_ROOT, 'manager/img/ticket_template_p.svg'))
    ticket_template.set_text('event_name', ticket_data['event'].name[:30])
    locale.setlocale(locale.LC_TIME, lang)  # Locale del request
    ticket_template.set_text('event_date', (ticket_data['event'].date.strftime("%A %d de %B de %Y")).decode('utf-8'))
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


def send_event_ticket(user, lang):
    ticket_svg = generate_ticket(user, lang)
    ticket_data = user.get_ticket_data()

    try:
        email = EmailMessage()
        subject = _(u"Ticket for %(event_name)s event") % {'event_name': ticket_data.event.name}
        body = _(u"Hello %(first_name)s %(last_name)s,\n Here is your ticket for %(event_name)s event. \
        Please remember to print it and bring it with you the day of the event. \
        \n Regards, FLISoL %(event_name)s team.") % {'event_name': ticket_data.event.name,
                                                     'first_name': ticket_data.first_name,
                                                     'last_name': ticket_data.last_name}
        email.subject = unicode(subject)
        email.body = unicode(body)
        email.to = [ticket_data.email]
        email.attach('Ticket-' + str(ticket_data.ticket.id).zfill(12) + '.pdf', cairosvg.svg2pdf(bytestring=ticket_svg),
                     'application/pdf')
        email.send(fail_silently=False)
        ticket_data.ticket.sent = True
        ticket_data.ticket.save()
    except Exception as e:
        ticket_data.ticket.sent = False
        ticket_data.ticket.save()
        raise e


def create_organizer(event_user):
    organizer = Organizer.objects.filter(eventUser=event_user).first()
    if organizer is None:
        organizer = Organizer.objects.create(eventUser=event_user)

    add_organizer_permissions(organizer.eventUser.user)
    organizer.save()
    return organizer


# Views


def index(request, event_slug):
    try:
        event = Event.objects.filter(slug__iexact=event_slug).first()
        if not event:
            return handler404(request)
        if event.external_url:
            msgs = messages.get_messages(request)
            if msgs:
                return render(request, 'base.html', update_event_info(event_slug, request, {messages: msgs}, event))

            return HttpResponseRedirect(event.external_url)

        talk_proposals = TalkProposal.objects.filter(activity__event=event, confirmed_talk=True) \
            .exclude(image__isnull=True) \
            .distinct()

        render_dict = {'talk_proposals': talk_proposals}
        return render(request, 'event/index.html', update_event_info(event_slug, request, render_dict, event))
    except Event.DoesNotExist:
        raise Http404(_("The event you're looking for does not exists."))


def event_view(request, event_slug, html='index.html'):
    return render(request, html, update_event_info(event_slug, request))


def home(request):
    events = Event.objects.all()
    return render(request, 'homepage.html', {'events': events})


def generate_datetime(request, event):
    post = None
    if request.POST:
        start_time = datetime.datetime.strptime(request.POST.get('start_date', None), '%I:%M %p')
        end_time = datetime.datetime.strptime(request.POST.get('end_date', None), '%I:%M %p')

        start_time_posta = datetime.datetime.combine(event.date, start_time.time())
        end_time_posta = datetime.datetime.combine(event.date, end_time.time())

        post = request.POST.copy()

        post['start_date'] = start_time_posta.strftime('%Y-%m-%d %H:%M:%S')
        post['end_date'] = end_time_posta.strftime('%Y-%m-%d %H:%M:%S')
    return post


def talk_registration(request, event_slug, pk):
    errors = []
    error = False
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)

    # FIXME: Esto es lo que se llama una buena chanchada!
    post = generate_datetime(request, event)

    # Fin de la chanchada

    talk_form = TalkForm(event_slug, post)
    proposal = TalkProposal.objects.filter(pk=pk).first()
    if not proposal:
        return handler404(request)
    forms = [talk_form]
    if request.POST:
        if talk_form.is_valid() and \
                Activity.room_available(request=request, instance=talk_form.instance, event_slug=event_slug):
            try:
                proposal.confirmed_talk = True
                activity = proposal.activity
                activity.start_date = post['start_date']
                activity.end_date = post['end_date']
                room = Room.objects.filter(pk=request.POST.get('room')).first()
                if not room:
                    return handler404(request)
                activity.room = room
                activity.confirmed = True
                activity.save()
                proposal.save()
                messages.success(request, _("The talk was registered successfully!"))
                return HttpResponseRedirect(reverse("talk_detail", args=[event_slug, proposal.pk]))
            except Exception:
                if proposal.activity.confirmed:
                    proposal.activity.confirmed = False
                    proposal.activity.save()
                if proposal.confirmed_talk:
                    proposal.confirmed_talk = False
                    proposal.save()
        errors = get_forms_errors(forms)
        error = True
        if errors:
            messages.error(request, _("The talk couldn't be registered (check form errors)"))
    comments = Comment.objects.filter(activity=proposal.activity)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})

    render_dict.update({'multipart': False, 'errors': errors, 'form': talk_form, 'error': error})
    return render(request,
                  'activities/talks/detail.html',
                  update_event_info(event_slug, request, render_dict))


@login_required
@user_passes_test(is_installer, 'installer_registration')
def installation(request, event_slug):
    installation_form = InstallationForm(event_slug, request.POST or None, prefix='installation')
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
def talk_proposal(request, event_slug, pk=None):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)

    if not event.talk_proposal_is_open:
        messages.error(request,
                       _("The talk proposal is already closed or the event is not accepting proposals through this "
                         "page. Please contact the Event Organization Team to submit it."))
        return HttpResponseRedirect(reverse('index', args=(event_slug,)))

    errors = []
    new_activity, new_proposal = None, None

    if pk:
        proposal = TalkProposal.objects.filter(pk=pk).first()
        if not proposal:
            return handler404(request)
        activity = proposal.activity
    else:
        activity = Activity(event=event)
        proposal = TalkProposal(activity=activity)
    activity_form = ActivityForm(request.POST or None, instance=activity)
    proposal_form = TalkProposalForm(request.POST or None, request.FILES or None, instance=proposal)
    forms = [activity_form, proposal_form]

    if request.POST:
        if activity_form.is_valid():
            try:
                new_activity = activity_form.save()
                if proposal_form.is_valid():
                    new_proposal = proposal_form.save()
                    new_proposal.activity = new_activity
                    new_proposal.save()
                    return HttpResponseRedirect(reverse('image_cropping', args=(event_slug, proposal.pk)))
            except Exception:
                pass
        if new_activity is not None:
            Activity.delete(new_activity)
        if new_proposal is not None:
            TalkProposal.delete(new_proposal)
        messages.error(request, _("The proposal couldn't be registered (check form errors)"))
        errors = get_forms_errors(forms)

    return render(request, 'activities/talks/proposal.html',
                  update_event_info(event_slug, request, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def activity(request, event_slug, pk=None):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)

    post = generate_datetime(request, event)
    errors = []
    new_activity = None
    activity = Activity.objects.filter(pk=pk).first() if pk else Activity(event=event)
    if not activity:
        return handler404(request)

    activity_form = ActivityCompleteForm(event_slug, post or None, instance=activity)
    forms = [activity_form]

    if request.POST:
        if activity_form.is_valid() and \
                Activity.room_available(request=request, instance=activity_form.instance, event_slug=event_slug):
            try:
                activity = activity_form.save()
                activity.confirmed = True
                activity.start_date = post['start_date']
                activity.end_date = post['end_date']
                room = Room.objects.filter(pk=request.POST.get('room')).first()
                if not room:
                    return handler404(request)
                activity.room = room
                activity.save()
                messages.success(request, _("The activity has been registered successfully"))
                return HttpResponseRedirect(reverse('activities', args=[event_slug]))
            except Exception:
                if new_activity is not None:
                    Activity.delete(new_activity)
                messages.error(request, _("The activity couldn't be registered (check form errors)"))
                errors = get_forms_errors(forms)

    return render(request, 'activities/activity.html',
                  update_event_info(event_slug, request, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def image_cropping(request, event_slug, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = ImageCroppingForm(request.POST or None, request.FILES, instance=proposal.image)
    if request.POST:
        if form.is_valid():
            # If a new file is being upload
            if request.FILES:
                # If clear home_image is clicked, delete the image
                if request.POST.get('image-clear') or request.FILES:
                    form.cleaned_data['image'] = None
                # Save the changes and redirect to upload a new one or crop the new one
                image = form.save()
                proposal.image = image
                proposal.save()
                messages.info(request, _("Please crop or upload a new image."))
                return HttpResponseRedirect(reverse('image_cropping', args=(event_slug, proposal.pk)))
            form.save()
            messages.success(request, _("The proposal has been registered successfully!"))
            return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, proposal.pk)))
        messages.error(request, _("The proposal couldn't be registered (check form errors)"))
    return render(request, 'activities/talks/proposal/image-cropping.html',
                  update_event_info(event_slug, request, {'form': form}))


def schedule(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    if not event.schedule_confirm:
        messages.info(request,
                      _("The schedule is not confirmed yet. Meanwhile, you can see the list of activity proposals."))
        return HttpResponseRedirect(reverse("activities", args=[event_slug]))

    rooms = Room.objects.filter(event=event)
    activities_confirmed = Activity.objects.filter(confirmed=True, event=event)
    if activities_confirmed:
        schedule = Schedule(list(rooms), list(activities_confirmed))
        return render(request, 'activities/schedule.html',
                      update_event_info(event_slug, request, event=event, render_dict={'schedule': schedule}))
    messages.warning(
        request,
        _("You don't have any confirmed activities. Please confirm the activities first and then confirm the schedule")
    )
    return activities(request, event_slug)


def activities(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    talks_list, proposals, activities_not_confirmed, activities_confirmed = [], [], [], []
    activities_list = Activity.objects.filter(event=event)
    for activity in activities_list:
        talk_proposal = TalkProposal.objects.filter(activity=activity).first()
        if talk_proposal:
            talks_list.append(talk_proposal) if talk_proposal.confirmed_talk else proposals.append(talk_proposal)
        else:
            activities_confirmed.append(activity) if activity.confirmed else activities_not_confirmed.append(activity)
    for proposal in proposals:
        setattr(proposal, 'form', TalkForm(event_slug, instance=proposal.activity))
        setattr(proposal, 'errors', [])
    return render(request, 'activities/activities_home.html',
                  update_event_info(event_slug, request, {'talks': talks_list, 'proposals': proposals,
                                                          'activities_confirmed': activities_confirmed,
                                                          'activities_not_confirmed': activities_not_confirmed,
                                                          'event': event}, event))


def activity_detail(request, event_slug, pk):
    proposal = TalkProposal.objects.filter(activity__pk=pk).first()
    if not proposal:
        return handler404(request)
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, proposal.pk)))


def talk_detail(request, event_slug, pk):
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, pk)))


def talk_delete(request, event_slug, pk):
    talk = TalkProposal.objects.filter(pk=pk).first()
    if not talk:
        return handler404(request)
    talk.talk_proposal.confirmed = False
    talk.talk_proposal.save()
    talk.delete()
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, talk.talk_proposal.pk)))


def proposal_detail(request, event_slug, pk):
    proposal = TalkProposal.objects.filter(pk=pk).first()
    if not proposal:
        return handler404(request)
    comments = Comment.objects.filter(activity=proposal.activity)
    render_dict = dict(comments=comments, comment_form=CommentForm(), proposal=proposal)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})
    if proposal.confirmed_talk:
        render_dict.update({'talk': proposal, 'form': TalkForm(event_slug, instance=proposal.activity),
                            'form_presentation': PresentationForm(instance=proposal), 'errors': []})
    else:
        render_dict.update({'form': TalkForm(event_slug, instance=proposal.activity), 'errors': []})
    return render(request, 'activities/talks/detail.html', update_event_info(event_slug, request, render_dict))


def upload_presentation(request, event_slug, pk):
    proposal = get_object_or_404(TalkProposal, pk=pk)
    form = PresentationForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        if form.is_valid():
            if request.FILES:
                if request.POST.get('presentation-clear') or request.FILES:
                    form.cleaned_data['presentation'] = None
            form.save()
            messages.success(request, _("The presentation has been uploaded successfully!"))
            return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, proposal.pk)))
        messages.error(request, _("The presentation couldn't be uploaded (check form errors)"))
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, pk)))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_search(request, event_slug):
    form = AttendeeSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            attendee = form.cleaned_data['attendee']
            if attendee:
                if attendee.attended:
                    messages.info(request, _('The attendee has already been registered correctly.'))
                else:
                    attendee.attended = True
                    attendee.save()
                    messages.success(request, _('The attendee has been successfully registered. Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=[event_slug]))
            else:
                return HttpResponseRedirect('/event/' + event_slug + '/registration/attendee/by-collaborator')
        messages.error(request, _("The attendee couldn't be registered (check form errors)"))

    return render(request, 'registration/attendee/search.html', update_event_info(event_slug, request, {'form': form}))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_registration(request, event_slug, pk):
    attendee = Attendee.objects.filter(pk=pk).first()

    if attendee:
        if attendee.attended:
            messages.info(request, _('The attendee has already been registered correctly.'))
        else:
            attendee.attended = True
            attendee.save()
            messages.success(request, _('The attendee has been successfully registered. Happy Hacking!'))
        return HttpResponseRedirect(reverse("attendee_search", args=[event_slug]))
    else:
        messages.error(request, _("The user isn't registered for this event."))
        return HttpResponseRedirect(reverse("attendee_search", args=[event_slug]))


@login_required
@user_passes_test(is_organizer, 'index')
def add_organizer(request, event_slug):
    form = RegisteredEventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['event_user']
            if event_user:
                organizer = create_organizer(event_user)
                messages.success(
                    request,
                    _("%s has been successfully added as an Organizer." % organizer.eventUser.user.username))
            return HttpResponseRedirect(reverse("add_organizer", args=[event_slug]))

        messages.error(request, _("Something went wrong (please check form errors)"))

    organizers = Organizer.objects.filter(eventUser__event__slug__iexact=event_slug)
    return render(request, 'event/organizers.html',
                  update_event_info(event_slug, request, {'form': form, 'organizers': organizers}))


@login_required
@user_passes_test(is_organizer, 'index')
def add_registration_people(request, event_slug):
    form = RegisteredEventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['event_user']
            if event_user:
                Collaborator.objects.get_or_create(eventUser=event_user)
                add_attendance_permission(event_user.user)
                messages.success(request,
                                 _("%s has been successfully added to manage attendance." % event_user.user.username))
            return HttpResponseRedirect(reverse("add_registration_people", args=[event_slug]))

        messages.error(request, _("Something went wrong (please check form errors)"))

    if Permission.objects.filter(codename='can_take_attendance').exists():
        permission = Permission.objects.get(codename='can_take_attendance')
        registration_people = Collaborator.objects.filter(eventUser__user__user_permissions=permission,
                                                          eventUser__event__slug__iexact=event_slug)
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
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Attendee.objects.filter(event=event, email__iexact=email).count() > 0:
                messages.error(request, _("The attendee is already registered for this event, use correct form"))
                return HttpResponseRedirect(reverse("attendee_search", args=(event_slug,)))
            try:
                form.save()
                messages.success(request, _('The attendee was successfully registered . Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=(event_slug,)))
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


@login_required
@user_passes_test(is_organizer, 'index')
def delete_comment(request, event_slug, pk, comment_pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    pklist = request.POST.getlist("delete") if not comment_pk else [comment_pk]
    for comment_pk in pklist:
        comment = Comment.objects.filter(pk=comment_pk).first()
        if comment:
            comment.delete()
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required
def add_comment(request, event_slug, pk):
    """Add a new comment."""
    proposal = TalkProposal.objects.filter(pk=pk).first()
    if not proposal:
        return handler404(request)
    comment = Comment(activity=proposal.activity, user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save(notify=True)
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required
def vote_proposal(request, event_slug, pk, vote):
    proposal = TalkProposal.objects.filter(pk=pk).first()
    if not proposal:
        return handler404(request)
    exits_vote = Vote.objects.get_for_user(proposal, request.user)
    if not exits_vote and vote in ("1", "0"):
        Vote.objects.record_vote(proposal, request.user, 1 if vote == '1' else -1)
    return proposal_detail(request, event_slug, pk)


@login_required
def cancel_vote(request, event_slug, pk):
    proposal = TalkProposal.objects.filter(pk=pk).first()
    if not proposal:
        return handler404(request)
    vote = Vote.objects.get_for_user(proposal, request.user)
    if vote:
        vote.delete()
    return proposal_detail(request, event_slug, pk)


@login_required
@user_passes_test(is_organizer, 'index')
def confirm_schedule(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    event.schedule_confirm = True
    event.save()
    return schedule(request, event_slug)


def titleFromVote(vote, event):
    proposal = TalkProposal.objects.filter(pk=vote.object_id, activity__event=event).first()
    if not proposal:
        return {}
    return proposal.activity.title


def reports(request, event_slug):
    confirmed_attendees_count, not_confirmed_attendees_count, speakers_count = 0, 0, 0

    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    votes = Vote.objects.all()
    installers = Installer.objects.filter(eventUser__event=event)
    installations = Installation.objects.filter(attendee__event=event)
    talks = TalkProposal.objects.filter(activity__event=event)
    collaborators = Collaborator.objects.filter(eventUser__event=event)
    attendees = Attendee.objects.filter(event=event)

    confirmed_attendees_count = Attendee.objects.filter(event=event).filter(attended=True).count()

    not_confirmed_attendees_count = Attendee.objects.filter(event=event).filter(attended=False).count()

    # TODO: Tener en cuenta que si se empiezan a cargar los Speakers en alguna instancia
    # Va a tener que revisarse esto mejor
    for talk in talks:
        speakers_count += len(talk.speakers_names.split(','))

    template_dict = {
        'confirmed_attendees_count': confirmed_attendees_count,
        'not_confirmed_attendees_count': not_confirmed_attendees_count,
        'confirmed_collaborators_count': collaborators.filter(eventUser__attended=True).count(),
        'not_confirmed_collaborators_count': collaborators.filter(eventUser__attended=False).count(),
        'confirmed_installers_count': installers.filter(eventUser__attended=True).count(),
        'not_confirmed_installers_count': installers.filter(eventUser__attended=False).count(),
        'speakers_count': Speaker.objects.filter(eventUser__event=event).count() + speakers_count,
        'organizers_count': Organizer.objects.filter(eventUser__event=event).count(),
        'talk_proposals_count': TalkProposal.objects.filter(activity__event=event).count(),
        'installations_count': Installation.objects.filter(attendee__event=event).count(),
        'votes_for_talk': count_by(votes, lambda vote: titleFromVote(vote, event), lambda vote: vote.vote),
        'installers_for_level': count_by(installers, lambda inst: inst.level),
        'installers_count': installers.count(),
        'installation_for_software': count_by(installations, lambda inst: inst.software.name),
        'registered_in_time': count_by(attendees, lambda attendee: attendee.registration_date.date())
    }
    return render(request, 'reports/dashboard.html', update_event_info(event_slug, request, render_dict=template_dict))


@login_required
def generic_registration(request, event_slug, registration_model, new_role_form, msg_success, msg_error, template):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)

    if not event.registration_is_open:
        return render(request, 'registration/closed-registration.html', update_event_info(event_slug, request))

    errors = []
    event_user = EventUser.objects.filter(event=event, user=request.user).first()
    if not event_user:
        event_user = EventUser(event=event, user=request.user)

    new_role = registration_model.objects.filter(eventUser=event_user)

    if new_role:
        # Ya esta registrado con ese "rol"
        messages.error(request, _("You are already registered for this event"))
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))

    new_role = registration_model(eventUser=event_user)
    if request.POST:
        event_user_form = EventUserRegistrationForm(request.POST, instance=event_user)
        new_role_form = new_role_form(request.POST, instance=new_role)
        forms = [event_user_form, new_role_form]
        if event_user_form.is_valid() and new_role_form.is_valid():
            try:
                event_user = event_user_form.save()
                new_role = new_role_form.save()
                new_role.eventUser = event_user
                new_role.save()

                #                if not event_user.ticket:
                #                    try:
                #                        send_event_ticket(event_user, request.META.get('LANG'))
                #                        event_user.ticket = True
                #                        event_user.save()
                #                        msg_success += unicode(_(". Please check your email for the corresponding ticket."))
                #                    except Exception:
                #                        msg_success += unicode(
                #                            _(" but we couldn't send you your ticket. Please, check it out from the menu."))
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


def registration(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)

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
                messages.success(request, _("You have successfully registered to attend"))
                return HttpResponseRedirect('/event/' + event_slug)
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


def attendee_confirm_email(request, event_slug):
    pass


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

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid():
            organizer = None
            eventUser = None
            the_event = None
            contacts = None
            try:
                the_event = event_form.save()
                eventUser = EventUser.objects.create(user=request.user, event=the_event)
                organizer = create_organizer(eventUser)
                contacts = contacts_formset.save(commit=False)

                for a_contact in contacts:
                    a_contact.event = the_event
                    a_contact.save()

                return HttpResponseRedirect('/event/' + the_event.slug)
            except Exception:
                if organizer is not None:
                    Organizer.delete(organizer)
                if eventUser is not None:
                    EventUser.delete(eventUser)
                if the_event is not None:
                    Event.delete(the_event)
                if contacts is not None:
                    for a_contact in contacts:
                        Contact.objects.delete(a_contact)

        messages.error(request, _("There is a problem with your event. Please check the form for errors."))
    return render(request,
                  'event/create.html', {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                        'contacts_formset': contacts_formset})


@login_required
@user_passes_test(is_organizer, 'index')
def edit_event(request, event_slug):
    event = Event.objects.filter(slug__iexact=event_slug).first()
    if not event:
        return handler404(request)
    event_form = EventForm(request.POST or None, prefix='event', instance=event)
    ContactsFormSet = modelformset_factory(Contact, form=ContactForm, can_delete=True)

    contacts_formset = ContactsFormSet(request.POST or None, prefix='contacts-form', queryset=event.contacts.all())

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid():
            try:
                the_event = event_form.save()
                contacts = contacts_formset.save(commit=False)

                for a_contact in contacts:
                    a_contact.event = the_event

                contacts_formset.save()

                return HttpResponseRedirect('/event/' + the_event.slug)
            except Exception:
                pass

        messages.error(request, _("There is a problem with your event. Please check the form for errors."))
    return render(request,
                  'event/create.html',
                  update_event_info(event_slug, request,
                                    {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                     'contacts_formset': contacts_formset}))


@login_required
@user_passes_test(is_organizer, 'index')
def rooms(request, event_slug):
    rooms_list = Room.objects.filter(event__slug__iexact=event_slug)
    return render(request, 'room/rooms.html', update_event_info(event_slug, request, {'rooms': rooms_list}))


@login_required
@user_passes_test(is_organizer, 'index')
def remove_room(request, event_slug, pk):
    room = Room.objects.filter(pk=pk).first()
    if not room:
        return handler404(request)
    activities = Activity.objects.filter(room=room)
    if activities.count() > 0:
        messages.error(request,
                       _("The room hasn't been removed successfully because the room has confirmed activities."))
    else:
        room.delete()
        messages.success(request, _("The room has been removed successfully!"))
    return HttpResponseRedirect(reverse('rooms', args=[event_slug]))


@login_required
@user_passes_test(is_organizer, 'index')
def add_room(request, event_slug, pk=None):
    room = None
    if pk:
        room = Room.objects.filter(pk=pk).first()
        if not room:
            return handler404(request)
        room_form = RoomForm(request.POST or None, instance=room)
    else:
        room_form = RoomForm(request.POST or None)
    if request.POST:
        if room_form.is_valid():
            try:
                room = room_form.save()
                event = Event.objects.filter(slug__iexact=event_slug).first()
                if not event:
                    return handler404(request)
                room.event = event
                room.save()
                messages.success(request, _("The room has been added successfully!"))
                return HttpResponseRedirect(reverse('rooms', args=[event_slug]))
            except Exception:
                if room is not None:
                    Room.delete(room)
        messages.error(request, "The room hasn't been added successfully. Please check the form for errors.")
    return render(request, 'room/add_room.html',
                  update_event_info(event_slug, request, {'form': room_form, 'errors': get_forms_errors([room_form])}))


@login_required
def view_ticket(request, event_slug):
    event_user = EventUser.objects.filter(event__slug__iexact=event_slug).filter(user=request.user).first()
    if event_user:
        print 'HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        print event_user.get_ticket_data()
        ticket = generate_ticket(event_user, request.META.get('LANG'))
        response = HttpResponse(cairosvg.svg2pdf(bytestring=ticket), content_type='application/pdf')
        response["Content-Disposition"] = 'filename=Ticket-' + str(event_user.id).zfill(12) + '.pdf'
        return response
    else:
        messages.error(request, "You are not registered for this event")
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))


def handler404(request):
    response = render_to_response(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(request, '500.html', {})
    response.status_code = 500
    return response


@login_required
@user_passes_test(is_organizer, 'index')
def draw(request, event_slug):
    users = Attendee.objects.filter(event__slug__iexact=event_slug, attended=True).order_by('?')
    users = [str(user) for user in users]
    return render(request, 'event/draw.html', update_event_info(event_slug, request, {'eventusers': users}))
