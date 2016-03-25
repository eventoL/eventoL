# encoding: UTF-8
import itertools

import autocomplete_light
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from generic_confirmation.views import confirm_by_get
from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, InstallerRegistrationForm, \
    TalkProposalForm, ContactMessageForm, ImageCroppingForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, InstallerRegistrationFromCollaboratorForm, \
    CommentForm, PresentationForm, EventUserRegistrationForm, AttendeeRegistrationForm, ActivityForm, TalkForm, \
    EventForm
from manager.models import *
from manager.schedule import Schedule
from manager.security import is_installer, is_organizer
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


def talk_registration(request, event_slug, pk):
    errors = []
    error = False
    activity = None
    event = Event.objects.get(slug__iexact=event_slug)

    # FIXME: Esto es lo que se llama una buena chanchada!
    post = None
    if request.POST:
        start_time = datetime.datetime.strptime(request.POST.get('start_date', None), '%H:%M')
        end_time = datetime.datetime.strptime(request.POST.get('end_date', None), '%H:%M')

        start_time_posta = datetime.datetime.combine(event.date, start_time.time())
        end_time_posta = datetime.datetime.combine(event.date, end_time.time())

        post = request.POST.copy()

        post['start_date'] = start_time_posta.strftime('%Y-%m-%d %H:%M:%S')
        post['end_date'] = end_time_posta.strftime('%Y-%m-%d %H:%M:%S')

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
                  'talks/detail.html',
                  update_event_info(event_slug, render_dict))


def room_available(request, talk_form, event_slug):
    activities_room = Activity.objects.filter(room=talk_form.room, event__slug__iexact=event_slug)
    if talk_form.start_date == talk_form.end_date:
        messages.error(request, _(
            "The talk wasn't registered successfully because schedule isn't available (start time equals end time)"))
        return False
    if talk_form.end_date < talk_form.start_date:
        messages.error(request, _(
            "The talk wasn't registered successfully because schedule isn't available (start time is after end time)"))
        return False

    one_second = datetime.timedelta(seconds=1)
    if activities_room.filter(
            end_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists() \
            or activities_room.filter(end_date__gt=talk_form.end_date, start_date__lt=talk_form.start_date).exists() \
            or activities_room.filter(
                start_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists() \
            or activities_room.filter(end_date=talk_form.end_date, start_date=talk_form.start_date).exists():
        messages.error(request,
                       _("The talk wasn't registered successfully because the room or schedule isn't available"))
        return False
    return True


@login_required(login_url='../accounts/login/')
def become_installer(request, event_slug):
    forms = []
    errors = []
    installer = None

    if request.POST:
        eventUser = EventUser.objects.get(user=request.user)
        installer_form = InstallerRegistrationFromCollaboratorForm(request.POST,
                                                                   instance=Installer(eventUser=eventUser))
        forms = [installer_form]
        if installer_form.is_valid():
            try:
                installer = installer_form.save()
                installer.save()
                messages.success(request, _("You've become an installer!"))
                return HttpResponseRedirect('/event/' + event_slug)
            except Exception as e:
                if installer is not None:
                    Installer.delete(installer)
        messages.error(request, _("You haven't become an installer (check form errors)"))
        errors = get_forms_errors(forms)

    else:
        installer_form = InstallerRegistrationFromCollaboratorForm(instance=Installer())
        forms = [installer_form]

    return render(request,
                  'registration/become_installer.html',
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required(login_url='./accounts/login/')
@user_passes_test(is_installer)
def installation(request, event_slug):
    installation_form = InstallationForm(event_slug, request.POST or None, prefix='installation')
    hardware_form = HardwareForm(request.POST or None, prefix='hardware')
    forms = [installation_form, hardware_form]
    errors = []
    if request.POST:
        if hardware_form.is_valid():
            hardware = hardware_form.save()
            install = None
            try:
                if installation_form.is_valid():
                    install = installation_form.save()
                    install.hardware = hardware
                    install.installer = Installer.objects.get(eventUser__user=request.user)
                    install.save()
                    messages.success(request, _("The installation has been registered successfully. Happy Hacking!"))
                    return HttpResponseRedirect('/event/' + event_slug)
                else:
                    if hardware is not None:
                        Hardware.delete(hardware)
            except Exception:
                if hardware is not None:
                    Hardware.delete(hardware)
                if install is not None:
                    Installation.delete(install)
        messages.error(request, _("The installation hasn't been registered successfully (check form errors)"))
        errors = get_forms_errors(forms)

    return render(request,
                  'installation/installation-form.html',
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


def confirm_registration(request, event_slug, token):
    messages.success(request, _(
        'Thanks for your confirmation! You don\'t need to bring any paper to the event. You\'ll be asked for the '
        'email you registered with'))
    return confirm_by_get(request, token, success_url='/event/' + event_slug)


@login_required(login_url='../../accounts/login/')
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

    return render(request, 'talks/proposal.html',
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required(login_url='../../../accounts/login/')
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
    return render(request, 'talks/proposal/image-cropping.html', update_event_info(event_slug, {'form': form}))


def schedule(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    if not event.schedule_confirm:
        messages.info(request, _("While the schedule this unconfirmed, you can only see the list of proposals."))
        return HttpResponseRedirect(reverse("talks", args=[event_slug]))

    rooms = Room.objects.filter(event=event)
    talks_confirmed = TalkProposal.objects.filter(confirmed_talk=True, activity__event=event)
    if talks_confirmed:
        schedule = Schedule(list(rooms), list(talks_confirmed))
        return render(request, 'talks/schedule.html',
                      update_event_info(event_slug, event=event, render_dict={'schedule': schedule}))
    messages.warning(_("You don't have confirmed talks, please confirm talks and after confirm schedule"))
    return talks(request, event_slug)


def talks(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    talks_list = TalkProposal.objects.filter(activity__event=event, confirmed_talk=True)
    proposals = TalkProposal.objects.filter(activity__event=event, confirmed_talk=False)
    for proposal in proposals:
        setattr(proposal, 'form', TalkForm(event_slug, instance=proposal.activity))
        setattr(proposal, 'errors', [])
    return render(request, 'talks/talks_home.html',
                  update_event_info(event_slug, {'talks': talks_list, 'proposals': proposals, 'event': event}, event))


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
    return render(request, 'talks/detail.html', update_event_info(event_slug, render_dict))


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


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_search(request, event_slug):
    form = AttendeeSearchForm(event_slug, request.POST or None)
    if request.POST:
        if form.is_valid():
            attendee = form.cleaned_data['attendee']
            if attendee:
                if attendee.eventUser.assisted:
                    messages.info(request, _('The attendee has already been registered correctly.'))
                else:
                    attendee.eventUser.assisted = True
                    attendee.eventUser.save()
                    messages.success(request, _('The attendee has been registered successfully. Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=[event_slug]))
            else:
                return HttpResponseRedirect('/event/' + event_slug + '/registration/attendee/by-collaborator')
        messages.error(request, _("The attendee hasn't been registered successfully (check form errors)"))

    return render(request, 'registration/attendee/search.html', update_event_info(event_slug, {'form': form}))


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_registration_by_collaborator(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    attendee = Attendee(eventUser__event=event)
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None, instance=attendee)
    if request.POST:
        if form.is_valid():
            attendee = form.save()
            attendee.assisted = True
            attendee.save()
            messages.success(request, _('The attendee has been registered successfully. Happy Hacking!'))
            return HttpResponseRedirect(reverse("attendee_search", args=(event_slug,)))
        messages.error(request, _("The attendee hasn't been registered successfully (check form errors)"))

    return render(request, 'registration/attendee/by-collaborator.html', update_event_info(event_slug, {'form': form}))


def contact(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    contact_message = ContactMessage()
    form = ContactMessageForm(request.POST or None, instance=contact_message)
    if request.POST:
        if form.is_valid():
            contact_message = form.save()
            send_mail(_("FLISoL Contact Message " + contact_message.name + " email " + contact_message.email),
                      contact_message.message,
                      contact_message.email,
                      recipient_list=[event.email, ],
                      fail_silently=False)
            contact_message.save()
            messages.success(request, _("The message has been sent."))
            return HttpResponseRedirect('/event/' + event_slug)
        messages.error(request, _("The message hasn't been sent."))

    return render(request, 'contact-message.html', update_event_info(event_slug, {'form': form}, event))


@login_required(login_url='../../../../../accounts/login/')
def delete_comment(request, event_slug, pk, comment_pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        pklist = request.POST.getlist("delete") if not comment_pk else [comment_pk]
        for comment_pk in pklist:
            Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required(login_url='../../../accounts/login/')
def add_comment(request, event_slug, pk):
    """Add a new comment."""
    comment = Comment(activity=TalkProposal.objects.get(pk=pk).activity, user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save(notify=True)
    return HttpResponseRedirect(reverse("proposal_detail", args=[event_slug, pk]))


@login_required(login_url='../../../../../accounts/login/')
def vote_proposal(request, event_slug, pk, vote):
    proposal = TalkProposal.objects.get(pk=pk)
    exits_vote = Vote.objects.get_for_user(proposal, request.user)
    if not exits_vote and vote in ("1", "0"):
        Vote.objects.record_vote(proposal, request.user, 1 if vote == '1' else -1)
    return proposal_detail(request, event_slug, pk)


@login_required(login_url='../../../../../accounts/login/')
def cancel_vote(request, event_slug, pk):
    proposal = TalkProposal.objects.get(pk=pk)
    vote = Vote.objects.get_for_user(proposal, request.user)
    if vote:
        vote.delete()
    return proposal_detail(request, event_slug, pk)


@login_required(login_url='../../accounts/login/')
def confirm_schedule(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    event.schedule_confirm = True
    event.save()
    return schedule(request, event_slug)


def reports(request, event_slug):
    return render(request, 'reports/dashboard.html', update_event_info(event_slug))


def generic_registration(request, event_slug, registration_model, registration_form, msg_success, msg_error, template):
    event = Event.objects.get(slug__iexact=event_slug)

    if not event.registration_is_open:
        return render(request, 'registration/closed-registration.html', update_event_info(event_slug))

    errors = []
    user, eventUser, registration = None, None, None
    user_form = UserRegistrationForm(request.POST or None)

    if request.POST:
        eventUser_form = EventUserRegistrationForm(request.POST)
        registration_form = registration_form(request.POST)
        forms = [user_form, eventUser_form, registration_form]
        if user_form.is_valid():
            try:
                user = user_form.save()
                if eventUser_form.is_valid():
                    eventUser = eventUser_form.save()
                    eventUser.user = user
                    eventUser.save()
                    if registration_form.is_valid():
                        registration = registration_form.save()
                        registration.eventUser = eventUser
                        registration.save()
                        messages.success(request, msg_success)
                        return HttpResponseRedirect('/event/' + event_slug)
            except Exception:
                pass
        if user is not None:
            User.delete(user)
        if eventUser is not None:
            EventUser.delete(eventUser)
        if registration is not None:
            registration_model.delete(registration)
        messages.error(request, msg_error)
        errors = get_forms_errors(forms)

    else:
        eventUser = EventUser(event=event)
        registration = registration_model(eventUser=eventUser)
        eventUser_form = EventUserRegistrationForm(instance=eventUser)
        registration_form = registration_form(instance=registration)
        forms = [user_form, eventUser_form, registration_form]

    return render(request,
                  template,
                  update_event_info(event_slug, {'forms': forms, 'errors': errors, 'multipart': False}))


def registration(request, event_slug):
    msg_success = _("We've sent you an email with the confirmation link. Please click or "
                    "copy and paste it in your browser to confirm the registration.")
    msg_error = _("The attendee hasn't been registered successfully (check form errors)")
    template = 'registration/attendee-registration.html'
    return generic_registration(request, event_slug, Attendee,
                                AttendeeRegistrationForm, msg_success, msg_error, template)


def installer_registration(request, event_slug):
    msg_success = _("You've been registered successfully!")
    msg_error = _("You haven't been registered successfully (check form errors)")
    template = 'registration/installer-registration.html'
    return generic_registration(request, event_slug, Installer,
                                InstallerRegistrationForm, msg_success, msg_error, template)


def collaborator_registration(request, event_slug):
    msg_success = _("You've been registered successfully!")
    msg_error = _("You haven't been registered successfully (check form errors)")
    template = 'registration/collaborator-registration.html'
    return generic_registration(request, event_slug, Collaborator,
                                CollaboratorRegistrationForm, msg_success, msg_error, template)


@login_required(login_url='../accounts/login/')
def create_event(request):
    event_form = EventForm(request.POST or None, prefix='event')
    ContactsFormSet = modelformset_factory(Contact, fields=('type', 'url', 'text'), can_delete=True)

    contacts_formset = ContactsFormSet(request.POST or None, prefix='contacts-form', queryset=Contact.objects.none())

    if request.POST:
        if event_form.is_valid() and contacts_formset.is_valid():
            try:
                the_event = event_form.save()
                eventUser = EventUser.objects.create(user=request.user, event=the_event)
                organizer = Organizer.objects.create(eventUser=eventUser)
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


@login_required(login_url='../accounts/login/')
@user_passes_test(is_organizer)
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
