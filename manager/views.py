# encoding: UTF-8
import itertools
import svglue
import cairosvg
import pyqrcode
import json
import os, io

import autocomplete_light
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from manager.forms import CollaboratorRegistrationForm, InstallationForm, HardwareForm, InstallerRegistrationForm, \
    EventUserSearchForm, AttendeeRegistrationByCollaboratorForm, CommentForm, PresentationForm, \
    EventUserRegistrationForm, AttendeeRegistrationForm, ActivityForm, TalkForm, RoomForm, \
    EventForm, ContactMessageForm, TalkProposalForm, ImageCroppingForm,\
    RegisteredEventUserSearchForm, ActivityCompleteForm
from manager.models import *
from manager.schedule import Schedule
from manager.security import is_installer, is_organizer, user_passes_test, add_attendance_permission, is_collaborator, \
    add_organizer_permissions
from voting.models import Vote

autocomplete_light.autodiscover()


def update_event_info(event_slug, render_dict=None, event=None):
    event = event or Event.objects.get(slug__iexact=event_slug)
    contacts = Contact.objects.filter(event=event)
    render_dict = render_dict or {}
    render_dict.update({
        'event_slug': event_slug,
        'event': event,
        'contacts': contacts
    })
    return render_dict


def index(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)

    if event.external_url:
        msgs = messages.get_messages(request)
        if msgs:
            return render(request, 'base.html', update_event_info(event_slug, {messages: msgs}, event))

        return HttpResponseRedirect(event.external_url)

    talk_proposals = TalkProposal.objects.filter(activity__event=event, confirmed_talk=True) \
        .exclude(image__isnull=True) \
        .distinct()

    render_dict = {'talk_proposals': talk_proposals}
    return render(request, 'event/index.html', update_event_info(event_slug, render_dict, event))


def event_view(request, event_slug, html='index.html'):
    return render(request, html, update_event_info(event_slug))


def home(request):
    events = Event.objects.all()
    return render(request, 'homepage.html', {'events': events})


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def generateDatetime(request, event):
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
    activity = None
    event = Event.objects.get(slug__iexact=event_slug)

    # FIXME: Esto es lo que se llama una buena chanchada!
    post = generateDatetime(request, event)

    # Fin de la chanchada

    talk_form = TalkForm(event_slug, post)
    proposal = TalkProposal.objects.get(pk=pk)
    forms = [talk_form]
    if request.POST:
        if talk_form.is_valid() and room_available(request, talk_form.instance, event_slug):
            try:
                proposal.confirmed_talk = True
                activity = proposal.activity
                activity.start_date = post['start_date']
                activity.end_date = post['end_date']
                activity.room = Room.objects.get(pk=request.POST.get('room', None))
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
            messages.error(request, _("The talk wasn't registered successfully (check form errors)"))
    comments = Comment.objects.filter(activity=proposal.activity)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})

    render_dict.update({'multipart': False, 'errors': errors, 'form': talk_form, 'error': error})
    return render(request,
                  'activities/talks/detail.html',
                  update_event_info(event_slug, render_dict))


def room_available(request, talk_form, event_slug):
    activities_room = Activity.objects.filter(room=talk_form.room, event__slug__iexact=event_slug)
    if talk_form.start_date == talk_form.end_date:
        messages.error(request, _(
            "The talk couldn't be registered because the schedule not available (start time equals end time)"))
        return False
    if talk_form.end_date < talk_form.start_date:
        messages.error(request, _(
            "The talk couldn't be registered because the schedule is not available (start time is after end time)"))
        return False

    one_second = datetime.timedelta(seconds=1)
    if activities_room.filter(
            end_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists() \
            or activities_room.filter(end_date__gt=talk_form.end_date, start_date__lt=talk_form.start_date).exists() \
            or activities_room.filter(
                start_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists() \
            or activities_room.filter(end_date=talk_form.end_date, start_date=talk_form.start_date).exists():
        messages.error(request,
                       _("The talk couldn't be registered because the room or the schedule is not available"))
        return False
    return True


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
                install = None
                install = installation_form.save()
                install.hardware = hardware
                install.installer = EventUser.objects.get(user=request.user)
                install.save()
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
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def talk_proposal(request, event_slug, pk=None):
    event = Event.objects.get(slug__iexact=event_slug)

    if not event.talk_proposal_is_open:
        messages.error(request,
                       _("The talk proposal is already close or the event is not accepting proposals through this"
                         "page. Please contact the Event Organization Team to submit it."))
        return HttpResponseRedirect(reverse('index', args=(event_slug,)))

    errors = []
    new_activity, new_proposal = None, None

    if pk:
        proposal = TalkProposal.objects.get(pk=pk)
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
        messages.error(request, _("The proposal hasn't been registered successfully (check form errors)"))
        errors = get_forms_errors(forms)

    return render(request, 'activities/talks/proposal.html',
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def activity(request, event_slug, pk=None):
    event = Event.objects.get(slug__iexact=event_slug)

    post = generateDatetime(request, event)
    errors = []
    new_activity = None
    activity = Activity.objects.get(pk=pk) if pk else Activity(event=event)

    activity_form = ActivityCompleteForm(event_slug, post or None, instance=activity)
    forms = [activity_form]

    if request.POST:
        if activity_form.is_valid() and room_available(request, activity_form.instance, event_slug):
            try:
                activity = activity_form.save()
                activity.confirmed = True
                activity.start_date = post['start_date']
                activity.end_date = post['end_date']
                activity.room = Room.objects.get(pk=request.POST.get('room', None))
                activity.save()
                messages.success(request, _("The activity has been registered successfully"))
                return HttpResponseRedirect(reverse('activities', args=[event_slug]))
            except Exception, e:
                if new_activity is not None:
                    Activity.delete(new_activity)
                messages.error(request, _("The activity hasn't been registered successfully (check form errors)"))
                errors = get_forms_errors(forms)

    return render(request, 'activities/activity.html',
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


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
        messages.error(request, _("The proposal hasn't been registered successfully (check form errors)"))
    return render(request, 'activities/talks/proposal/image-cropping.html', update_event_info(event_slug, {'form': form}))


def schedule(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    if not event.schedule_confirm:
        messages.info(request, _("While the schedule this unconfirmed, you can only see the list of proposals."))
        return HttpResponseRedirect(reverse("activities", args=[event_slug]))

    rooms = Room.objects.filter(event=event)
    activities_confirmed = Activity.objects.filter(confirmed=True, event=event)
    if activities_confirmed:
        schedule = Schedule(list(rooms), list(activities_confirmed))
        return render(request, 'activities/schedule.html',
                      update_event_info(event_slug, event=event, render_dict={'schedule': schedule}))
    messages.warning(_("You don't have confirmed talks, please confirm talks and after confirm schedule"))
    return activities(request, event_slug)


def activities(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
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
                  update_event_info(event_slug, {'talks': talks_list, 'proposals': proposals,
                                                 'activities_confirmed': activities_confirmed,
                                                 'activities_not_confirmed': activities_not_confirmed,
                                                 'event': event}, event))


def talk_detail(request, event_slug, pk):
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, pk)))


def talk_delete(request, event_slug, pk):
    talk = TalkProposal.objects.get(pk=pk)
    talk.talk_proposal.confirmed = False
    talk.talk_proposal.save()
    talk.delete()
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, talk.talk_proposal.pk)))


def proposal_detail(request, event_slug, pk):
    proposal = TalkProposal.objects.get(pk=pk)
    comments = Comment.objects.filter(activity=proposal.activity)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})
    if proposal.confirmed_talk:
        render_dict.update({'talk': proposal, 'form': TalkForm(event_slug, instance=proposal.activity),
                            'form_presentation': PresentationForm(instance=proposal), 'errors': []})
    else:
        render_dict.update({'form': TalkForm(event_slug, instance=proposal.activity), 'errors': []})
    return render(request, 'activities/talks/detail.html', update_event_info(event_slug, render_dict))


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
        messages.error(request, _("The presentation hasn't been uploaded successfully (check form errors)"))
    return HttpResponseRedirect(reverse('proposal_detail', args=(event_slug, pk)))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_search(request, event_slug):
    form = EventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            eventUser = form.cleaned_data['eventUser']
            if eventUser:
                if eventUser.assisted:
                    messages.info(request, _('The attendee has already been registered correctly.'))
                else:
                    eventUser.assisted = True
                    eventUser.save()
                    messages.success(request, _('The attendee has been successfully registered. Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=[event_slug]))
            else:
                return HttpResponseRedirect('/event/' + event_slug + '/registration/attendee/by-collaborator')
        messages.error(request, _("The attendee hasn't been successfully registered (check form errors)"))

    return render(request, 'registration/attendee/search.html', update_event_info(event_slug, {'form': form}))


@login_required
@user_passes_test(is_organizer, 'index')
def add_organizer(request, event_slug):
    form = RegisteredEventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['eventUser']
            if event_user:
                organizer = create_organizer(event_user)
                messages.success(request,
                                 _("%s has been successfully added as an Organizer." % event_user.user.username))
            return HttpResponseRedirect(reverse("add_organizer", args=[event_slug]))

        messages.error(request, _("Something went wrong (please check form errors)"))

    organizers = Organizer.objects.filter(eventUser__event__slug__iexact=event_slug)
    return render(request, 'event/organizers.html',
                  update_event_info(event_slug, {'form': form, 'organizers': organizers}))


@login_required
@user_passes_test(is_organizer, 'index')
def add_registration_people(request, event_slug):
    form = RegisteredEventUserSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            event_user = form.cleaned_data['eventUser']
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
                  update_event_info(event_slug, {'form': form, 'registration_people': registration_people}))


@login_required
@permission_required('manager.can_take_attendance', raise_exception=True)
@user_passes_test(is_collaborator, 'collaborator_registration')
def attendee_registration_by_collaborator(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    attendee = NonRegisteredAttendee()
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None, instance=attendee)
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data["email"]
            if EventUser.objects.filter(event=event, user__email=email).count() > 0:
                messages.error(request, _("The attendee has registered for this event, use correct form"))
                return HttpResponseRedirect(reverse("attendee_search", args=(event_slug,)))
            if EventUser.objects.filter(event=event, nonregisteredattendee__email=email).count() > 0:
                form.add_error('email', _("Email already registered for this event"))
            try:
                form.save()
                eventuser = EventUser(event=event, nonregisteredattendee=attendee, assisted=True)
                eventuser.save()
                if form.cleaned_data["is_installing"]:
                    installer = InstallationAttendee(eventUser=eventuser,
                                                     installation_additional_info=form.cleaned_data[
                                                         "installation_additional_info"])
                    installer.save()
                else:
                    attendee = Attendee(eventUser=eventuser)
                    attendee.save()
                messages.success(request, _('The attendee was successfully registered . Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=(event_slug,)))
            except:
                pass
        messages.error(request, _("The attendee couldn't be registered (check form errors)"))
    return render(request, 'registration/attendee/by-collaborator.html', update_event_info(event_slug, {'form': form}))


def contact(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
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
            contact_message.event = Event.objects.get(slug__iexact=event_slug)
            contact_message.save()
            messages.success(request, _("The message has been sent. You will receive a reply by email"))
            return HttpResponseRedirect('/event/' + event_slug)
        messages.error(request, _("There was a problem sending your message. Please try again in a few minutes."))

    return render(request, 'contact-message.html', update_event_info(event_slug, {'form': form}, event))


@login_required
@user_passes_test(is_organizer, 'index')
def delete_comment(request, event_slug, pk, comment_pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    pklist = request.POST.getlist("delete") if not comment_pk else [comment_pk]
    for comment_pk in pklist:
        Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required
def add_comment(request, event_slug, pk):
    """Add a new comment."""
    comment = Comment(activity=TalkProposal.objects.get(pk=pk).activity, user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save(notify=True)
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required
def vote_proposal(request, event_slug, pk, vote):
    proposal = TalkProposal.objects.get(pk=pk)
    exits_vote = Vote.objects.get_for_user(proposal, request.user)
    if not exits_vote and vote in ("1", "0"):
        Vote.objects.record_vote(proposal, request.user, 1 if vote == '1' else -1)
    return proposal_detail(request, event_slug, pk)


@login_required
def cancel_vote(request, event_slug, pk):
    proposal = TalkProposal.objects.get(pk=pk)
    vote = Vote.objects.get_for_user(proposal, request.user)
    if vote:
        vote.delete()
    return proposal_detail(request, event_slug, pk)


@login_required
@user_passes_test(is_organizer, 'index')
def confirm_schedule(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    event.schedule_confirm = True
    event.save()
    return schedule(request, event_slug)


def reports(request, event_slug):
    return render(request, 'reports/dashboard.html', update_event_info(event_slug))


def generate_ticket(eventUser):
    ticket_template = svglue.load(file=os.path.join(settings.STATIC_ROOT, 'manager/img/ticket_template_p.svg'))
    ticket_template.set_text('event_name', eventUser.event.name[:30])
    ticket_template.set_text('event_date', eventUser.event.date.strftime("%A %d de %B de %Y"))
    place = json.loads(eventUser.event.place)
    if place.get("name"):  # Si tiene nombre cargado
        ticket_template.set_text('event_place_name', place.get("name"))
        ticket_template.set_text('event_place_address', place.get("formatted_address"))
    else:
        ticket_template.set_text('event_place_name', place.get("formatted_address"))
        ticket_template.set_text('event_place_address', '')

    ticket_template.set_text('ticket_type', u'Entrada General')
    qr = pyqrcode.create(eventUser.id)
    code = io.BytesIO()
    qr.png(code, scale=7, quiet_zone=0)
    ticket_template.set_image('qr_code', code.getvalue(), mimetype='image/png')
    ticket_template.set_text('eventUser_PK', str(eventUser.id).zfill(12))
    ticket_template.set_text('eventUser_email', eventUser.user.email)  # No se enviara a los NonRegisteredAttendee

    userName_l1 = u"%s %s" % (eventUser.user.first_name, eventUser.user.last_name)
    userName_l2 = ''
    if (len(userName_l1) > 30):
        userName_l1 = eventUser.user.first_name[:30]  # Por si tiene mas de 30 caracteres
        userName_l2 = eventUser.user.last_name[:30]

    ticket_template.set_text('eventUser_name_l1', userName_l1)
    ticket_template.set_text('eventUser_name_l2', userName_l2)

    return str(ticket_template)


def send_event_ticket(eventUser):
    ticket = generate_ticket(eventUser)

    email = EmailMessage()
    email.subject = unicode(_("Ticket for %s event" % (eventUser.event.name)))
    email.body = unicode(_("Hello %s %s,\n Here is your ticket for %s event. \
    Please remember to print it and bring it with you the day of the event. \
    \n Regards, %s team." % (
        eventUser.user.first_name, eventUser.user.last_name, eventUser.event.name, eventUser.event.name)))
    email.to = [eventUser.user.email]
    email.attach('Ticket-' + str(eventUser.id).zfill(12) + '.pdf', cairosvg.svg2pdf(bytestring=ticket),
                 'application/pdf')
    email.send(fail_silently=False)


@login_required
def generic_registration(request, event_slug, registration_model, registration_form, msg_success, msg_error, template):
    event = Event.objects.get(slug__iexact=event_slug)

    if not event.registration_is_open:
        return render(request, 'registration/closed-registration.html', update_event_info(event_slug))

    errors = []
    eventUser = EventUser.objects.filter(event=event, user=request.user).first()
    if not eventUser:
        eventUser = EventUser(event=event, user=request.user)

    registration = registration_model.objects.filter(eventUser=eventUser)

    # FIXME: Chanchada
    installation = InstallationAttendee.objects.filter(eventUser=eventUser)

    if registration or installation:
        # Ya esta registrado con ese "rol"
        messages.error(request, "You are already registered for this event")
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))

    registration = registration_model(eventUser=eventUser)
    if request.POST:
        eventUser_form = EventUserRegistrationForm(request.POST, instance=eventUser)
        registration_form = registration_form(request.POST, instance=registration)
        forms = [eventUser_form, registration_form]
        if eventUser_form.is_valid() and registration_form.is_valid():
            try:
                eventUser = eventUser_form.save()
                # FIXME: Chanchada
                if registration_model is Attendee and registration_form.cleaned_data["is_installing"]:
                    installation = InstallationAttendee(eventUser=eventUser,
                                                        installation_additional_info=registration_form.cleaned_data[
                                                            "installation_additional_info"])
                    installation.save()
                else:
                    registration = registration_form.save()
                    registration.eventUser = eventUser
                    registration.save()

                if not eventUser.ticket:
                    try:
                        send_event_ticket(eventUser)
                        eventUser.ticket = True
                        eventUser.save()
                        msg_success += ". Please check your email for the corresponding ticket."
                    except Exception:
                        msg_success += " but we couldn't send you your ticket. Please, check it out from the menu."
                messages.success(request, msg_success)
                return HttpResponseRedirect('/event/' + event_slug)
            except Exception:
                pass
        messages.error(request, msg_error)
    else:
        eventUser_form = EventUserRegistrationForm(instance=eventUser)
        registration_form = registration_form(instance=registration)
        forms = [eventUser_form, registration_form]

    return render(request,
                  template,
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def registration(request, event_slug):
    msg_success = _("You have successfully registered to attend")
    msg_error = _("There is a problem with the registration (check form errors)")
    template = 'registration/attendee-registration.html'
    return generic_registration(request, event_slug, Attendee,
                                AttendeeRegistrationForm, msg_success, msg_error, template)


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
    ContactsFormSet = modelformset_factory(Contact, fields=('type', 'url', 'text'), can_delete=True)

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

        messages.error(request, "There is a problem with your event. Please check the form for errors.")
    return render(request,
                  'event/create.html', {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                        'contacts_formset': contacts_formset}, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_organizer, 'index')
def edit_event(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    event_form = EventForm(request.POST or None, prefix='event', instance=event)
    ContactsFormSet = modelformset_factory(Contact, fields=('type', 'url', 'text'), can_delete=True)

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

        messages.error(request, "There is a problem with your event. Please check the form for errors.")
    return render(request,
                  'event/create.html',
                  update_event_info(event_slug,
                                    {'form': event_form, 'domain': request.get_host(), 'protocol': request.scheme,
                                     'contacts_formset': contacts_formset}), context_instance=RequestContext(request))


@login_required
@user_passes_test(is_organizer, 'index')
def rooms(request, event_slug):
    rooms_list = Room.objects.filter(event__slug__iexact=event_slug)
    return render(request, 'room/rooms.html', update_event_info(event_slug, {'rooms': rooms_list}))


@login_required
@user_passes_test(is_organizer, 'index')
def remove_room(request, event_slug, pk):
    room = Room.objects.get(pk=pk)
    activities = Activity.objects.filter(room=room)
    if activities.count() > 0:
        messages.error(request, "The room hasn't been removed successfully because the room have confirmed activities.")
    else:
        room.delete()
        messages.success(request, _("The room has been removed successfully!"))
    return HttpResponseRedirect(reverse('rooms', args=[event_slug]))


@login_required
@user_passes_test(is_organizer, 'index')
def add_room(request, event_slug, pk=None):
    room = None
    if pk:
        room = Room.objects.get(pk=pk)
        room_form = RoomForm(request.POST or None, instance=room)
    else:
        room_form = RoomForm(request.POST or None)
    if request.POST:
        if room_form.is_valid():
            try:
                room = room_form.save()
                room.event = Event.objects.get(slug__iexact=event_slug)
                room.save()
                messages.success(request, _("The room has been added successfully!"))
                return HttpResponseRedirect(reverse('rooms', args=[event_slug]))
            except Exception:
                if room is not None:
                    Room.delete(room)
        messages.error(request, "The room hasn't been added successfully. Please check the form for errors.")
    return render(request, 'room/add_room.html',
                  update_event_info(event_slug, {'form': room_form, 'errors': get_forms_errors([room_form])}))


@login_required
def view_ticket(request, event_slug):
    eventuser = EventUser.objects.filter(event__slug__iexact=event_slug).filter(user=request.user).first()
    if eventuser:
        ticket = generate_ticket(eventuser)
        response = HttpResponse(cairosvg.svg2pdf(bytestring=ticket), content_type='application/pdf')
        response["Content-Disposition"] = 'filename=Ticket-' + str(eventuser.id).zfill(12) + '.pdf'
        return response
    else:
        messages.error(request, "You are not registered for this event")
        return HttpResponseRedirect(reverse("index", args=(event_slug,)))


def create_organizer(event_user):
    organizer = Organizer.objects.create(eventUser=event_user)
    add_organizer_permissions(organizer.eventUser.user)
    organizer.save()
    return organizer
