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
    AttendantSearchForm, AttendantRegistrationByCollaboratorForm
from manager.models import Installer, Hardware, Installation, Talk, Room, \
    TalkTime, TalkType, TalkProposal, Sede, Attendant, Organizer
from manager.security import add_installer_perms


autocomplete_light.autodiscover()


def index(request, sede_url):
    talk_proposals = TalkProposal.objects.filter(sede__url=sede_url) \
        .exclude(home_image__isnull=True) \
        .exclude(home_image__exact='') \
        .exclude(dummy_talk=True)

    # Seguro hay una mejor forma de hacerlo
    # estoy saliendo de un apuro :P
    titles = []
    filtered = []
    for t in talk_proposals:
        if t.title not in titles:
            filtered.append(t)
            titles.append(t.title)

    return render(request, 'index.html', {'talk_proposals': filtered, 'sede_url': sede_url})


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
            except:
                User.delete(user)
        errors = get_forms_errors(forms)

    return render(request,
                  'registration/collaborator-registration.html',
                  {'forms': forms, 'errors': errors, 'multipart': False, 'sede_url': sede_url})


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
                  {'forms': forms, 'errors': errors, 'multipart': False, 'sede_url': sede_url})


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
                  {'forms': forms, 'errors': errors, 'multipart': False, 'sede_url': sede_url})


def registration(request, sede_url):
    form = RegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/registration/confirm')
    else:
        sede = Sede.objects.get(url=sede_url)
        attendant = Attendant(sede=sede)
        form = RegistrationForm(instance=attendant)

    return render(request, 'registration/attendant-registration.html', {'form': form, 'sede_url': sede_url})


@login_required
def talk_proposal(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    proposal = TalkProposal(sede=sede)
    form = TalkProposalForm(request.POST or None, request.FILES or None, instance=proposal)
    if request.POST:
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse('image_cropping', args=(sede_url, proposal.pk)))

    return render(request, 'talks/proposal.html', {'form': form, 'sede_url': sede_url})


@login_required
def image_cropping(request, sede_url, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = TalkProposalImageCroppingForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        # FIXME No me acuerdo por qué este if: if not proposal.cropping:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/talk/confirm')
    return render(request, 'talks/proposal/image-cropping.html', {'form': form, 'sede_url': sede_url})


# FIXME: Esto es lo que hay que tirar y hacer de nuevo :)
def talks(request, sede_url):
    class TalksTable(tables.Table):
        hour = tables.Column(verbose_name=_('Hour'), orderable=False)


    if Talk.objects.all().count() == 0:
        return render(request, "talks/schedule.html", {'tables': None, 'sede_url': sede_url})

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

    return render(request, "talks/schedule.html", {'tables': tabless, 'sede_url': sede_url})


@login_required
@permission_required('manager.add_attendant', raise_exception=True)
def attendant_search(request, sede_url):
    form = AttendantSearchForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            attendant_email = form.cleaned_data['attendant']
            if attendant_email is not None:
                attendant = Attendant.objects.get(email=attendant_email, sede__url=sede_url)
                attendant.assisted = True
                attendant.save()
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendant/assisted')
            else:
                return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendant/by-collaborator')

    return render(request, 'registration/attendant/search.html', {'form': form, 'sede_url': sede_url})


@login_required
@permission_required('manager.add_attendant', raise_exception=True)
def attendant_registration_by_collaborator(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    attendee = Attendant(sede=sede)
    form = AttendantRegistrationByCollaboratorForm(request.POST or None, instance=attendee)
    if request.POST:
        if form.is_valid():
            attendee = form.save()
            attendee.assisted = True
            attendee.save()
            return HttpResponseRedirect('/sede/' + sede_url + '/registration/attendant/assisted')

    return render(request, 'registration/attendant/by-collaborator.html', {'form': form, 'sede_url': sede_url})


class TalkDetailView(DetailView):
    model = Talk
    template_name = 'talks/detail.html'
