# encoding: UTF-8
import itertools

import autocomplete_light
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext as _
import django_tables2 as tables

from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, RegistrationForm, InstallerRegistrationForm, \
    TalkProposalForm, TalkProposalImageCroppingForm, \
    AttendeeSearchForm, AttendeeRegistrationByCollaboratorForm, InstallerRegistrationFromCollaboratorForm
from manager.models import Installer, Hardware, Installation, Talk, Room, \
    TalkTime, TalkType, TalkProposal, Sede, Attendee, Organizer
from manager.security import add_installer_perms


autocomplete_light.autodiscover()


def update_sede_info(sede_url, render_dict=None, sede=None):
    if not sede:
        sede = Sede.objects.get(url=sede_url)
    render_dict = render_dict or {}
    render_dict.update({
        'sede_url': sede_url,
        'footer': sede.footer,
        'event_information': sede.event_information
    })
    return render_dict


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
    return render(request, 'home.html')


def get_forms_errors(forms):
    field_errors = [form.non_field_errors() for form in forms]
    errors = [error for error in field_errors]
    return list(itertools.chain.from_iterable(errors))


def collaborator_registration(request, sede_url):
    user_form = UserRegistrationForm(request.POST or None)
    if request.POST:
        collaborator_form = CollaboratorRegistrationForm(request.POST)
    else:
        sede = Sede.objects.get(url=sede_url)
        organizer = Organizer(sede=sede)
        collaborator_form = CollaboratorRegistrationForm(instance=organizer)

    forms = [user_form, collaborator_form]
    errors = []

    if request.POST:
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

    return render(request,
                  'registration/collaborator-registration.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


def installer_registration(request, sede_url):
    user_form = UserRegistrationForm(request.POST or None)
    if request.POST:
        installer_form = InstallerRegistrationForm(request.POST)
    else:
        sede = Sede.objects.get(url=sede_url)
        installer = Installer(sede=sede)
        installer_form = InstallerRegistrationForm(instance=installer)

    forms = [user_form, installer_form]
    errors = []
    if request.POST:
        if user_form.is_valid():
            user = user_form.save()
            try:
                if installer_form.is_valid():
                    installer = installer_form.save()
                    user = add_installer_perms(user)
                    installer.user = user
                    installer.save()
                    return HttpResponseRedirect('/sede/' + sede_url + '/registration/success')
            except Exception as e:
                if user is not None:
                    User.delete(user)
                if installer is not None:
                    Installer.delete(installer)
        errors = get_forms_errors(forms)

    return render(request,
                  'registration/installer-registration.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
def become_installer(request, sede_url):
    errors = []
    installer = None
    if request.POST:
        user = User.objects.get_by_natural_key(request.user.username)
        installer_form = InstallerRegistrationFromCollaboratorForm(request.POST, instance=user)
    else:
        installer = Installer()
        installer_form = InstallerRegistrationFromCollaboratorForm(instance=installer)

    forms = [installer_form]
    if request.POST:
        try:
            if installer_form.is_valid():
                installer = installer_form.save()
                user = add_installer_perms(user)
                installer.user = user
                installer.save()
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/success')
        except Exception as e:
            if installer is not None:
                Installer.delete(installer)
        errors = get_forms_errors(forms)

    return render(request,
                  'registration/become_installer.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


@login_required
@permission_required('manager.add_installation', raise_exception=True)
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
                    installer = Installer.objects.filter(user__username=request.user.username)[0]
                    installation.installer = installer
                    installation.save()
                    return HttpResponseRedirect('/sede/' + sede_url + '/installation/success')
            except:
                if hardware is not None:
                    Hardware.delete(hardware)
                if installation is not None:
                    Installation.delete(installation)
        errors = get_forms_errors(forms)
    return render(request,
                  'installation/installation-form.html',
                  update_sede_info(sede_url, {'forms': forms, 'errors': errors, 'multipart': False}))


def registration(request, sede_url):
    form = RegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/registration/confirm')
    else:
        sede = Sede.objects.get(url=sede_url)
        attendee = Attendee(sede=sede)
        form = RegistrationForm(instance=attendee)

    return render(request, 'registration/attendee-registration.html', update_sede_info(sede_url, {'form': form}))


@login_required
def talk_proposal(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    proposal = TalkProposal(sede=sede)
    form = TalkProposalForm(request.POST or None, request.FILES or None, instance=proposal)
    if request.POST:
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse('image_cropping', args=(sede_url, proposal.pk)))

    return render(request, 'talks/proposal.html', update_sede_info(sede_url, {'form': form}))


@login_required
def image_cropping(request, sede_url, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = TalkProposalImageCroppingForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        # FIXME No me acuerdo por qué este if: if not proposal.cropping:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/talk/confirm')
    return render(request, 'talks/proposal/image-cropping.html', update_sede_info(sede_url, {'form': form}))


# FIXME: Esto es lo que hay que tirar y hacer de nuevo :)
def talks(request, sede_url):
    class TalksTable(tables.Table):
        hour = tables.Column(verbose_name=_('Hour'), orderable=False)

    if Talk.objects.all().count() == 0:
        return render(request, "talks/schedule.html", update_sede_info(sede_url, {'tables': None}))

    tabless = {}
    for sede in Sede.objects.all():
        for talk_type in TalkType.objects.all():
            rooms = Room.objects.filter(for_type=talk_type, sede=sede)
            talks = []
            attrs = dict((room.name, tables.Column(orderable=False)) for room in rooms)
            attrs['Meta'] = type('Meta', (), dict(attrs={"class": "table", "orderable": "False", }))
            klass = type('DynamicTable', (TalksTable,), attrs)

            hours = TalkTime.objects.filter(talk_type=talk_type, sede=sede).order_by('start_date')
            
            for hour in hours:
                talkss = Talk.objects.filter(hour=hour, sede=sede)
                talk = {'hour': hour}
                for t in talkss:
                    
                    talk_link = '<a href="' + reverse('talk_detail', args=[t.pk]) \
                                + '" data-toggle="modal" data-target="#modal">' + t.title + '</a>'
                    for speaker in t.speakers.all():
                        if not speaker.user.first_name == '':
                            talk_link += (' - ' + ' '.join((speaker.user.first_name, speaker.user.last_name)))
                    
                    talk[t.room.name] = mark_safe(talk_link)
                talks.append(talk)

            table = klass(talks)
            if len(talks) > 0:
                sede_key = ''.join((str(sede.date.day), '/', str(sede.date.month), ' - ', sede.name,))
                if sede_key not in tabless:
                    tabless[sede_key] = {}
                tabless[sede_key][talk_type.name] = table

    return render(request, "talks/schedule.html", update_sede_info(sede_url, {'tables': tabless}))


@login_required
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


@login_required
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


class TalkDetailView(DetailView):
    model = Talk
    template_name = 'talks/detail.html'
