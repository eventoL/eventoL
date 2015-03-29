# encoding: UTF-8
import itertools
import datetime

import autocomplete_light
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from manager import security

from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, RegistrationForm, InstallerRegistrationForm, \
    TalkProposalForm, TalkProposalImageCroppingForm, ContactMessageForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, InstallerRegistrationFromCollaboratorForm,\
    TalkForm, CommentForm
from manager.models import Installer, Hardware, Installation, Talk, \
    TalkProposal, Sede, Attendee, Collaborator, ContactMessage, Comment
from manager.security import add_installer_perms
from voting.models import Vote


autocomplete_light.autodiscover()


def update_sede_info(sede_url, render_dict=None, sede=None):
    sede = sede or Sede.objects.get(url=sede_url)
    render_dict = render_dict or {}
    render_dict.update({
        'sede_url': sede_url,
        'footer': sede.footer,
        'event_information': sede.event_information
    })
    return render_dict


def login(request, sede_url):
    return django_login(request, extra_context=update_sede_info(sede_url))


def index(request, sede_url):
    sede = Sede.objects.get(url=sede_url)

    talk_proposals = sede.talk_proposals.exclude(home_image__isnull=True) \
        .exclude(home_image__exact='') \
        .exclude(dummy_talk=True) \
        .distinct()

    render_dict = {'talk_proposals': talk_proposals, 'contacts': sede.contacts.all()}
    return render(request, 'index.html', update_sede_info(sede_url, render_dict, sede))


def sede_view(request, sede_url, html='home.html'):
    return render(request, html, update_sede_info(sede_url))


def event(request, sede_url):
    return render(request, 'event/info.html', update_sede_info(sede_url))


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
                    collaborator.user = user
                    collaborator.save()
                    return HttpResponseRedirect('/sede/' + sede_url + '/registration/success')
            except Exception:
                User.delete(user)
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
    talk_form = TalkForm(request.POST or None)
    proposal = TalkProposal.objects.get(pk=pk)
    forms = [talk_form]
    if request.POST:
        if talk_form.is_valid() and room_available(talk_form.instance, sede_url):
            try:
                proposal.confirmed = True
                proposal.save()
                talk = talk_form.save()
                talk.talk_proposal = proposal
                talk.save()
                return HttpResponseRedirect(reverse("manager.views.talk_detail", args=[sede_url, talk.pk]))
            except Exception:
                if talk is not None:
                    Talk.delete(talk)
                if proposal.confirmed:
                    proposal.confirmed = False
                    proposal.save()
        errors = get_forms_errors(forms)
        error = True
    comments = Comment.objects.filter(proposal=proposal)
    render_dict = dict(comments=comments, comment_form=CommentForm(), user=request.user, proposal=proposal)
    render_dict.update({'multipart': False, 'errors': errors, 'form': talk_form, 'error': error})
    return render(request,
                  'talks/detail.html',
                  update_sede_info(sede_url, render_dict))


def room_available(talk_form, sede_url):
    talks_room = Talk.objects.filter(room=talk_form.room, talk_proposal__sede__name=sede_url)
    if talks_room.filter(start_date__range=(talk_form.start_date, talk_form.end_date)).exists()\
            or talks_room.filter(end_date__range=(talk_form.start_date, talk_form.end_date)).exists()\
            or talks_room.filter(end_date__gte=talk_form.end_date, start_date__lte=talk_form.start_date).exists():
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
        try:
            if user_form.is_valid():
                user = user_form.save()
                if collaborator_form.is_valid():
                    collaborator = collaborator_form.save()
                    if installer_form.is_valid():
                            installer = installer_form.save()
                            user = add_installer_perms(user)
                            collaborator.user = user
                            collaborator.save()
                            installer.collaborator = collaborator
                            installer.save()
                            return HttpResponseRedirect('/sede/' + sede_url + '/registration/success')
        except Exception as e:
            if user is not None:
                User.delete(user)
            if collaborator is not None:
                Collaborator.delete(collaborator)
            if installer is not None:
                Installer.delete(installer)
        errors = get_forms_errors(forms)

    else:
        sede = Sede.objects.get(url=sede_url)
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
        collaborator = Collaborator.objects.get(user__username=request.user.username)
        installer_form = InstallerRegistrationFromCollaboratorForm(request.POST,
                                                                   instance=Installer(collaborator=collaborator))
        forms = [installer_form]
        if installer_form.is_valid():
            try:
                installer = installer_form.save()
                collaborator.user = add_installer_perms(collaborator.user)
                collaborator.save()
                installer.save()
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/success')
            except Exception as e:
                if installer is not None:
                    Installer.delete(installer)
        errors = get_forms_errors(forms)

    else:
        installer_form = InstallerRegistrationFromCollaboratorForm(instance=Installer())
        forms = [installer_form]

    return render(request,
                  'registration/become_installer.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required(login_url='./accounts/login/')
@permission_required('manager.add_installation', raise_exception=True)
@user_passes_test(security.is_installer)
def installation(request, sede_url):
    installation_form = InstallationForm(request.POST or None, prefix='installation')
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
                    installation.installer = Installer.objects.get(collaborator__user__username=request.user.username)
                    installation.save()
                    return HttpResponseRedirect('/sede/' + sede_url + '/installation/success')
            except Exception:
                if hardware is not None:
                    Hardware.delete(hardware)
                if installation is not None:
                    Installation.delete(installation)
        errors = get_forms_errors(forms)
    return render(request,
                  'installation/installation-form.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


def registration(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    if sede.date < datetime.date.today():
        return render(request, 'registration/closed-registration.html', update_sede_info(sede_url))
    form = RegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/registration/confirm')
    else:
        attendee = Attendee(sede=sede)
        form = RegistrationForm(instance=attendee)

    return render(request, 'registration/attendee-registration.html', update_sede_info(sede_url, {'form': form}))


@login_required(login_url='../../accounts/login/')
def talk_proposal(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    proposal = TalkProposal(sede=sede)
    form = TalkProposalForm(request.POST or None, request.FILES or None, instance=proposal)
    if request.POST:
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse('image_cropping', args=(sede_url, proposal.pk)))

    return render(request, 'talks/proposal.html', update_sede_info(sede_url, {'form': form}))


@login_required(login_url='../../../accounts/login/')
def image_cropping(request, sede_url, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = TalkProposalImageCroppingForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        # FIXME No me acuerdo por qué este if: if not proposal.cropping:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/talk/confirm')
    return render(request, 'talks/proposal/image-cropping.html', update_sede_info(sede_url, {'form': form}))


def schedule(request, sede_url):
    pass


def talks(request, sede_url):
    sede = Sede.objects.get(name=sede_url)
    if datetime.date.today() > sede.limit_proposal_date:
        return HttpResponseRedirect(reverse("manager.views.schedule", args=[sede_url]))
    talks_list = Talk.objects.filter(talk_proposal__sede__name=sede_url)
    proposals = TalkProposal.objects.filter(sede__name=sede_url)
    for proposal in proposals:
        setattr(proposal, 'form', TalkForm())
        setattr(proposal, 'errors', [])
    return render(request, 'talks/talks_home.html',
                  update_sede_info(sede_url, {'talks': talks_list, 'proposals': proposals}))


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
        render_dict.update({'form': TalkForm(), 'errors': []})
    return render(request, 'talks/detail.html', update_sede_info(sede_url, render_dict))


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_search(request, sede_url):
    form = AttendeeSearchForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            attendee_email = form.cleaned_data['attendee']
            if attendee_email is not None:
                attendee = Attendee.objects.get(email=attendee_email, sede__url=sede_url)
                attendee.assisted = True
                attendee.save()
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendee/assisted')
            else:
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendee/by-collaborator')

    return render(request, 'registration/attendee/search.html', update_sede_info(sede_url, {'form': form}))


@login_required(login_url='../../accounts/login/')
@permission_required('manager.add_attendee', raise_exception=True)
def attendee_registration_by_collaborator(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    attendee = Attendee(sede=sede)
    form = AttendeeRegistrationByCollaboratorForm(request.POST or None, instance=attendee)
    if request.POST:
        if form.is_valid():
            attendee = form.save()
            attendee.assisted = True
            attendee.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendee/assisted')

    return render(request, 'registration/attendee/by-collaborator.html', update_sede_info(sede_url, {'form': form}))


def contact(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
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
            return HttpResponseRedirect('/sede/' + sede_url)
    return render(request, 'contact-message.html', update_sede_info(sede_url, {'form': form}, sede))


@login_required(login_url='../../../../../accounts/login/')
def delete_comment(request, sede_url, pk, comment_pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        pklist = request.POST.getlist("delete") if not comment_pk else [comment_pk]
        for comment_pk in pklist:
            Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect(reverse("manager.views.proposal_detail", args=[sede_url, pk]))


@login_required(login_url='../../../accounts/login/')
def add_comment(request, sede_url, pk):
    """Add a new comment."""
    comment = Comment(proposal=TalkProposal.objects.get(pk=pk), user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.save(notify=True)
    return HttpResponseRedirect(reverse("manager.views.proposal_detail", args=[sede_url, pk]))


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
