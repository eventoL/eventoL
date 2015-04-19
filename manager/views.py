# encoding: UTF-8
import itertools
import datetime

import autocomplete_light
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from voting.models import Vote
from generic_confirmation.views import confirm_by_get

from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, RegistrationForm, InstallerRegistrationForm, \
    TalkProposalForm, TalkProposalImageCroppingForm, ContactMessageForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, InstallerRegistrationFromCollaboratorForm, \
    TalkForm, CommentForm
from manager.models import Installer, Hardware, Installation, Talk, \
    TalkProposal, Sede, Attendee, Collaborator, ContactMessage, Comment, Contact, Room
from manager.schedule import Schedule
from manager.security import is_installer, add_collaborator_perms


autocomplete_light.autodiscover()


def update_sede_info(sede_url, render_dict=None, sede=None):
    sede = sede or Sede.objects.get(url__iexact=sede_url)
    contacts = Contact.objects.filter(sede=sede)
    render_dict = render_dict or {}
    render_dict.update({
        'sede_url': sede_url,
        'sede': sede,
        'contacts': contacts
    })
    return render_dict


def sede_django_view(request, sede_url, view=django_login):
    return view(request, extra_context=update_sede_info(sede_url))


def index(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)

    if sede.external_url:
        msgs = messages.get_messages(request)
        if msgs:
            return render(request, 'base.html', update_sede_info(sede_url, {messages: msgs}, sede))

        return HttpResponseRedirect(sede.external_url)

    talk_proposals = sede.talk_proposals.exclude(home_image__isnull=True) \
        .exclude(home_image__exact='') \
        .exclude(dummy_talk=True) \
        .distinct()

    render_dict = {'talk_proposals': talk_proposals}
    return render(request, 'index.html', update_sede_info(sede_url, render_dict, sede))


def sede_view(request, sede_url, html='index.html'):
    return render(request, html, update_sede_info(sede_url))


def event(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)

    if sede.external_url:
        return HttpResponseRedirect(sede.external_url)

    render_dict = update_sede_info(sede_url, render_dict={'event_information': sede.event_information}, sede=sede)
    return render(request, 'event/info.html', render_dict)


def home(request):
    sedes = Sede.objects.all()
    return render(request, 'homepage.html', {'sedes': sedes})


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def collaborator_registration(request, sede_url):
    errors = []
    user_form = UserRegistrationForm(request.POST or None)

    if request.POST:
        collaborator_form = CollaboratorRegistrationForm(request.POST)
        forms = [user_form, collaborator_form]
        if user_form.is_valid():
            user = user_form.save()
            try:
                if collaborator_form.is_valid():
                    collaborator = collaborator_form.save()
                    user = add_collaborator_perms(user)
                    user.save()
                    collaborator.user = user
                    collaborator.save()
                    messages.success(request, _("You've been registered successfully!"))
                    return HttpResponseRedirect('/sede/' + sede_url)
            except Exception:
                User.delete(user)
        messages.error(request, _("You haven't been registered successfully (check form errors)"))
        errors = get_forms_errors(forms)

    else:
        sede = Sede.objects.get(url=sede_url)
        collaborator = Collaborator(sede=sede)
        collaborator_form = CollaboratorRegistrationForm(instance=collaborator)
        forms = [user_form, collaborator_form]

    return render(request,
                  'registration/collaborator-registration.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


def talk_registration(request, sede_url, pk):
    errors = []
    error = False
    talk = None
    sede = Sede.objects.get(url__iexact=sede_url)

    # FIXME: Esto es lo que se llama una buena chanchada!
    post = None
    if request.POST:
        start_time = datetime.datetime.strptime(request.POST.get('start_date', None), '%H:%M')
        end_time = datetime.datetime.strptime(request.POST.get('end_date', None), '%H:%M')

        start_time_posta = datetime.datetime.combine(sede.date, start_time.time())
        end_time_posta = datetime.datetime.combine(sede.date, end_time.time())

        post = request.POST.copy()

        post['start_date'] = start_time_posta.strftime('%Y-%m-%d %H:%M:%S')
        post['end_date'] = end_time_posta.strftime('%Y-%m-%d %H:%M:%S')

    # Fin de la chanchada

    talk_form = TalkForm(sede_url, post)
    proposal = TalkProposal.objects.get(pk=pk)
    forms = [talk_form]
    if request.POST:
        if talk_form.is_valid() and room_available(request, talk_form.instance, sede_url):
            try:
                proposal.confirmed = True
                proposal.save()
                talk = talk_form.save()
                talk.talk_proposal = proposal
                talk.save()
                messages.success(request, _("The talk was registered successfully!"))
                return HttpResponseRedirect(reverse("talk_detail", args=[sede_url, talk.pk]))
            except Exception:
                if talk is not None:
                    Talk.delete(talk)
                if proposal.confirmed:
                    proposal.confirmed = False
                    proposal.save()
        errors = get_forms_errors(forms)
        error = True
        if errors:
            messages.error(request, _("The talk wasn't registered successfully (check form errors)"))
    comments = Comment.objects.filter(proposal=proposal)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})

    render_dict.update({'multipart': False, 'errors': errors, 'form': talk_form, 'error': error})
    return render(request,
                  'talks/detail.html',
                  update_sede_info(sede_url, render_dict))


def room_available(request, talk_form, sede_url):
    talks_room = Talk.objects.filter(room=talk_form.room, talk_proposal__sede__url__iexact=sede_url)
    if talk_form.start_date == talk_form.end_date:
        messages.error(request, _(
            "The talk wasn't registered successfully because schedule isn't available (start time equals end time)"))
        return False
    if talk_form.end_date < talk_form.start_date:
        messages.error(request, _(
            "The talk wasn't registered successfully because schedule isn't available (start time is after end time)"))
        return False

    one_second = datetime.timedelta(seconds=1)
    if talks_room.filter(
            end_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists() \
            or talks_room.filter(end_date__gt=talk_form.end_date, start_date__lt=talk_form.start_date).exists() \
            or talks_room.filter(
                    start_date__range=(talk_form.start_date + one_second, talk_form.end_date - one_second)).exists():
        messages.error(request,
                       _("The talk wasn't registered successfully because the room or schedule isn't available"))
        return False
    return True


def installer_registration(request, sede_url):
    errors = []
    user, collaborator, installer = None, None, None
    user_form = UserRegistrationForm(request.POST or None)

    if request.POST:
        collaborator_form = CollaboratorRegistrationForm(request.POST)
        installer_form = InstallerRegistrationForm(request.POST)
        forms = [user_form, collaborator_form, installer_form]
        if user_form.is_valid():
            try:
                user = user_form.save()
                if collaborator_form.is_valid():
                    collaborator = collaborator_form.save()
                    if installer_form.is_valid():
                        installer = installer_form.save()
                        collaborator.user = add_collaborator_perms(user)
                        collaborator.save()
                        installer.collaborator = collaborator
                        installer.save()
                        messages.success(request, _("You've been registered successfully!"))
                        return HttpResponseRedirect('/sede/' + sede_url)
            except Exception:
                pass
        if user is not None:
            User.delete(user)
        if collaborator is not None:
            Collaborator.delete(collaborator)
        if installer is not None:
            Installer.delete(installer)
        messages.error(request, _("You haven't been registered successfully (check form errors)"))
        errors = get_forms_errors(forms)

    else:
        sede = Sede.objects.get(url__iexact=sede_url)
        installer = Installer()
        collaborator = Collaborator(sede=sede)
        collaborator_form = CollaboratorRegistrationForm(instance=collaborator)
        installer_form = InstallerRegistrationForm(instance=installer)
        forms = [user_form, collaborator_form, installer_form]

    return render(request,
                  'registration/installer-registration.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required(login_url='../accounts/login/')
def become_installer(request, sede_url):
    forms = []
    errors = []
    installer = None

    if request.POST:
        collaborator = Collaborator.objects.get(user=request.user)
        installer_form = InstallerRegistrationFromCollaboratorForm(request.POST,
                                                                   instance=Installer(collaborator=collaborator))
        forms = [installer_form]
        if installer_form.is_valid():
            try:
                installer = installer_form.save()
                collaborator.user = add_collaborator_perms(collaborator.user)
                collaborator.save()
                installer.save()
                messages.success(request, _("You've became an installer!"))
                return HttpResponseRedirect('/sede/' + sede_url)
            except Exception as e:
                if installer is not None:
                    Installer.delete(installer)
        messages.error(request, _("You not became an installer (check form errors)"))
        errors = get_forms_errors(forms)

    else:
        installer_form = InstallerRegistrationFromCollaboratorForm(instance=Installer())
        forms = [installer_form]

    return render(request,
                  'registration/become_installer.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required(login_url='./accounts/login/')
@user_passes_test(is_installer)
def installation(request, sede_url):
    installation_form = InstallationForm(sede_url, request.POST or None, prefix='installation')
    hardware_form = HardwareForm(request.POST or None, prefix='hardware')
    forms = [installation_form, hardware_form]
    errors = []
    if request.POST:
        if hardware_form.is_valid():
            hardware = hardware_form.save()
            try:
                if installation_form.is_valid():
                    installation = installation_form.save()
                    installation.hardware = hardware
                    installation.installer = Installer.objects.get(collaborator__user=request.user)
                    installation.save()
                    messages.success(request, _("The installation has been registered successfully. Happy Hacking!"))
                    return HttpResponseRedirect('/sede/' + sede_url)
            except Exception:
                pass

        if hardware is not None:
            Hardware.delete(hardware)
        if installation is not None:
            Installation.delete(installation)

        messages.error(request, _("The installation hasn't been registered successfully (check form errors)"))
        errors = get_forms_errors(forms)
    return render(request,
                  'installation/installation-form.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


def registration(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    if not sede.registration_is_open:
        return render(request, 'registration/closed-registration.html', update_sede_info(sede_url))
    form = RegistrationForm(request.POST or None, domain=request.get_host(), protocol=request.scheme)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, _(
                "We've sent you an email with the confirmation link. Please click or copy and paste it in your "
                "browser to confirm the registration."))
            return HttpResponseRedirect('/sede/' + sede_url)
        messages.error(request, _("The attendee hasn't been registered successfully (check form errors)"))
    else:
        attendee = Attendee(sede=sede)
        form = RegistrationForm(instance=attendee)

    return render(request, 'registration/attendee-registration.html', update_sede_info(sede_url, {'form': form}))


def confirm_registration(request, sede_url, token):
    messages.success(request, _(
        'Thanks for your confirmation! You don\'t need to bring any paper to the event. You\'ll be asked for the '
        'email you registered with'))
    return confirm_by_get(request, token, success_url='/sede/' + sede_url)


@login_required(login_url='../../accounts/login/')
def talk_proposal(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)

    if not sede.talk_proposal_is_open:
        messages.error(request,
                       _(
                           "The talk proposal is already close or the sede is not accepting proposals through this "
                           "page. Please contact the Sede Organization Team to submit it."))
        return HttpResponseRedirect(reverse('index', args=(sede_url,)))

    proposal = TalkProposal(sede=sede)
    form = TalkProposalForm(request.POST or None, request.FILES or None, instance=proposal)
    if request.POST:
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse('image_cropping', args=(sede_url, proposal.pk)))
        messages.error(request, _("The proposal hasn't been registered successfully (check form errors)"))

    return render(request, 'talks/proposal.html', update_sede_info(sede_url, {'form': form}))


@login_required(login_url='../../../accounts/login/')
def image_cropping(request, sede_url, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = TalkProposalImageCroppingForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        if form.is_valid():
            # If a new file is being upload
            if request.FILES:
                # If clear home_image is clicked, delete the image
                if request.POST.get('home_image-clear') or request.FILES:
                    form.cleaned_data['home_image'] = None

                # Save the changes and redirect to upload a new one or crop the new one
                form.save()
                messages.info(request, _("Please crop or upload a new image."))
                return HttpResponseRedirect(reverse('image_cropping', args=(sede_url, proposal.pk)))
            form.save()
            messages.success(request, _("The proposal has been registered successfully!"))
            return HttpResponseRedirect(reverse('proposal_detail', args=(sede_url, proposal.pk)))
        messages.error(request, _("The proposal hasn't been registered successfully (check form errors)"))
    return render(request, 'talks/proposal/image-cropping.html', update_sede_info(sede_url, {'form': form}))


def schedule(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    if not sede.schedule_confirm:
        messages.info(request, _("While the schedule this unconfirmed, you can only see the list of proposals."))
        return HttpResponseRedirect(reverse("talks", args=[sede_url]))

    rooms = Room.objects.filter(sede=sede)
    talks_confirmed = Talk.objects.filter(talk_proposal__confirmed=True, talk_proposal__sede=sede)
    schedule = Schedule(list(rooms), list(talks_confirmed))
    return render(request, 'talks/schedule.html',
                  update_sede_info(sede_url, sede=sede, render_dict={'schedule': schedule}))


def talks(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    talks_list = Talk.objects.filter(talk_proposal__sede=sede)
    proposals = TalkProposal.objects.filter(sede=sede)
    for proposal in proposals:
        setattr(proposal, 'form', TalkForm(sede_url))
        setattr(proposal, 'errors', [])
    return render(request, 'talks/talks_home.html',
                  update_sede_info(sede_url, {'talks': talks_list, 'proposals': proposals, 'sede': sede}, sede))


def talk_detail(request, sede_url, pk):
    talk = Talk.objects.get(pk=pk)
    return proposal_detail(request, sede_url, talk.talk_proposal.pk)


def proposal_detail(request, sede_url, pk):
    proposal = TalkProposal.objects.get(pk=pk)
    comments = Comment.objects.filter(proposal=proposal)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    vote = Vote.objects.get_for_user(proposal, request.user)
    score = Vote.objects.get_score(proposal)
    if vote or score:
        render_dict.update({'vote': vote, 'score': score})
    if proposal.confirmed:
        talk = Talk.objects.get(talk_proposal=proposal)
        render_dict.update({'talk': talk})
    else:
        render_dict.update({'form': TalkForm(sede_url), 'errors': []})
    return render(request, 'talks/detail.html', update_sede_info(sede_url, render_dict))


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_search(request, sede_url):
    form = AttendeeSearchForm(sede_url, request.POST or None)
    if request.POST:
        if form.is_valid():
            attendee_email = form.cleaned_data['attendee']
            if attendee_email is not None:
                attendee = Attendee.objects.get(email=attendee_email, sede__url__iexact=sede_url)
                if attendee.assisted:
                    messages.info(request, _('The attendee has already been registered correctly.'))
                else:
                    attendee.assisted = True
                    attendee.save()
                    messages.success(request, _('The attendee has been registered successfully. Happy Hacking!'))
                return HttpResponseRedirect(reverse("attendee_search", args=[sede_url]))
            else:
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendee/by-collaborator')
        messages.error(request, _("The attendee hasn't been registered successfully (check form errors)"))

    return render(request, 'registration/attendee/search.html', update_sede_info(sede_url, {'form': form}))


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_registration_by_collaborator(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    attendee = Attendee(sede=sede)
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None, instance=attendee)
    if request.POST:
        if form.is_valid():
            attendee = form.save()
            attendee.assisted = True
            attendee.save()
            messages.success(request, _('The attendee has been registered successfully. Happy Hacking!'))
            return HttpResponseRedirect(reverse("attendee_search", args=(sede_url, )))
        messages.error(request, _("The attendee hasn't been registered successfully (check form errors)"))

    return render(request, 'registration/attendee/by-collaborator.html', update_sede_info(sede_url, {'form': form}))


def contact(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    contact_message = ContactMessage()
    form = ContactMessageForm(request.POST or None, instance=contact_message)
    if request.POST:
        if form.is_valid():
            contact_message = form.save()
            send_mail(_("FLISoL Contact Message " + contact_message.name + " email " + contact_message.email),
                      contact_message.message,
                      contact_message.email,
                      recipient_list=[sede.email, ],
                      fail_silently=False)
            contact_message.save()
            messages.success(request, _("The message has been sent."))
            return HttpResponseRedirect('/sede/' + sede_url)
        messages.error(request, _("The message hasn't been sent."))

    return render(request, 'contact-message.html', update_sede_info(sede_url, {'form': form}, sede))


@login_required(login_url='../../../../../accounts/login/')
def delete_comment(request, sede_url, pk, comment_pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        pklist = request.POST.getlist("delete") if not comment_pk else [comment_pk]
        for comment_pk in pklist:
            Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect(reverse("proposal_detail", args=[sede_url, pk]))


@login_required(login_url='../../../accounts/login/')
def add_comment(request, sede_url, pk):
    """Add a new comment."""
    comment = Comment(proposal=TalkProposal.objects.get(pk=pk), user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save(notify=True)
    return HttpResponseRedirect(reverse("proposal_detail", args=[sede_url, pk]))


@login_required(login_url='../../../../../accounts/login/')
def vote_proposal(request, sede_url, pk, vote):
    proposal = TalkProposal.objects.get(pk=pk)
    exits_vote = Vote.objects.get_for_user(proposal, request.user)
    if not exits_vote and vote in ("1", "0"):
        Vote.objects.record_vote(proposal, request.user, 1 if vote == '1' else -1)
    return proposal_detail(request, sede_url, pk)


@login_required(login_url='../../../../../accounts/login/')
def cancel_vote(request, sede_url, pk):
    proposal = TalkProposal.objects.get(pk=pk)
    vote = Vote.objects.get_for_user(proposal, request.user)
    if vote:
        vote.delete()
    return proposal_detail(request, sede_url, pk)


@login_required(login_url='../../accounts/login/')
def confirm_schedule(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    sede.schedule_confirm = True
    sede.save()
    return schedule(request, sede_url)
