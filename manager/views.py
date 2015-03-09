# encoding: UTF-8
import autocomplete_light
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView
import itertools
from django.utils.translation import ugettext as _

import django_tables2 as tables
from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, RegistrationForm, InstallerRegistrationForm, \
    TalkProposalForm, TalkProposalImageCroppingForm, \
    AttendantSearchForm, AttendantRegistrationByCollaboratorForm
from manager.models import Installer, Hardware, Installation, Talk, Room, \
    TalkTime, TalkType, TalkProposal, Sede, Attendant
from manager.security import add_installer_perms


autocomplete_light.autodiscover()


def home(request):
    talk_proposals = TalkProposal.objects.exclude(home_image__isnull=True).exclude(home_image__exact='').exclude(
        dummy_talk=True)

    # Seguro hay una mejor forma de hacerlo
    # estoy saliendo de un apuro :P
    titles = []
    filtered = []
    for t in talk_proposals:
        if t.title not in titles:
            filtered.append(t)
            titles.append(t.title)

    return render(request, 'index.html', {'talk_proposals': filtered})


def collaborator_registration(request):
    user_form = UserRegistrationForm(request.POST or None)
    collaborator_form = CollaboratorRegistrationForm(request.POST or None)
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
                    return HttpResponseRedirect('/app/registration/success')
            except:
                User.delete(user)
        errors = list(itertools.chain.from_iterable([error for error in [form.non_field_errors() for form in forms]]))

    return render(request, 'registration/collaborator-registration.html', {'forms': forms,
                                                                           'errors': errors,
                                                                           'multipart': False, })


def installer_registration(request):
    user_form = UserRegistrationForm(request.POST or None)
    installer_form = InstallerRegistrationForm(request.POST or None)
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
                    return HttpResponseRedirect('/app/registration/success')
            except:
                if user is not None: User.delete(user)
                if installer is not None: Installer.delete(installer)
        errors = list(itertools.chain.from_iterable([error for error in [form.non_field_errors() for form in forms]]))

    return render(request, 'registration/installer-registration.html', {'forms': forms,
                                                                        'errors': errors,
                                                                        'multipart': False, })


@login_required
@permission_required('manager.add_installation', raise_exception=True)
def installation(request):
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
                    return HttpResponseRedirect('/app/installation/success')
            except:
                if hardware is not None: Hardware.delete(hardware)
                if installation is not None: Installation.delete(installation)
        errors = list(itertools.chain.from_iterable([error for error in [form.non_field_errors() for form in forms]]))
    return render(request, 'installation/installation-form.html', {'forms': forms,
                                                                   'errors': errors,
                                                                   'multipart': False, })


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/registration/confirm')
    else:
        form = RegistrationForm()

    return render(request, 'registration/attendant-registration.html', {'form': form})


@login_required
def talk_proposal(request):
    form = TalkProposalForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse('image_cropping', args=(proposal.pk,)))

    return render(request, 'talks/proposal.html', {'form': form, })


@login_required
def image_cropping(request, image_id):
    proposal = get_object_or_404(TalkProposal, pk=image_id)
    form = TalkProposalImageCroppingForm(request.POST or None, request.FILES, instance=proposal)
    if request.POST:
        if not proposal.cropping:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/app/talk/confirm')
    return render(request, 'talks/proposal/image-cropping.html', {'form': form})


def talks(request):
    class TalksTable(tables.Table):
        hour = tables.Column(verbose_name=_('Hour'), orderable=False)


    if Talk.objects.all().count() == 0:
        return render(request, "talks/schedule.html", {'tables': None})

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
                    
                    talk_link = '<a href="' + reverse('talk_detail', args=[
                        t.pk]) + '" data-toggle="modal" data-target="#modal">' + t.title + '</a>'
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

    return render(request, "talks/schedule.html", {'tables': tabless})


@login_required
@permission_required('manager.add_attendant', raise_exception=True)
def attendant_search(request):
    form = AttendantSearchForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            attendant_email = form.cleaned_data['attendant']
            sede = form.cleaned_data['sede']
            if attendant_email is not None:
                attendant = Attendant.objects.get(email=attendant_email, sede__pk=sede)
                attendant.assisted = True
                attendant.save()
                return HttpResponseRedirect('/app/registration/attendant/assisted')
            else:
                return HttpResponseRedirect('/app/registration/attendant/by-collaborator')

    return render(request, 'registration/attendant/search.html', {'form': form, })


@login_required
@permission_required('manager.add_attendant', raise_exception=True)
def attendant_registration_by_collaborator(request):
    form = AttendantRegistrationByCollaboratorForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            attendant = form.save()
            attendant.assisted = True
            attendant.save()
            return HttpResponseRedirect('/app/registration/attendant/assisted')

    return render(request, 'registration/attendant/by-collaborator.html', {'form': form})


class TalkDetailView(DetailView):
    model = Talk
    template_name = 'talks/detail.html'
