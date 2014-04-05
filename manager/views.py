# encoding: UTF-8
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import itertools

import django_tables2 as tables
import autocomplete_light
autocomplete_light.autodiscover()
from manager.forms import UserRegistrationForm, CollaboratorRegistrationForm, \
    InstallationForm, HardwareForm, RegistrationForm, InstallerRegistrationForm, \
    TalkProposalForm, TalkProposalImageCroppingForm
from manager.models import Installer, Hardware, Installation, Talk, Room, \
    TalkTime, TalkType, TalkProposal
from manager.security import add_installer_perms
from django.core.urlresolvers import reverse


def home(request):
    return render(request, 'index.html', {'talk_proposals': TalkProposal.objects.all()})


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
                if hardware is not None:Hardware.delete(hardware)
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
        hour = tables.Column()


    if Talk.objects.all().count() == 0:
        return render(request, "talks/schedule.html", {'tables': None})

    tabless = {}
    for talk_type in TalkType.objects.all():
        rooms = Room.objects.filter(for_type=talk_type)
        talks = []
        attrs = dict((room.name, tables.Column()) for room in rooms)
        attrs['Meta'] = type('Meta', (), dict(attrs={"class":"table", "orderable":"False", }))
        klass = type('DynamicTable', (TalksTable,), attrs)

        hours = TalkTime.objects.filter(talk_type=talk_type)

        for hour in hours:
            talkss = Talk.objects.filter(hour=hour)
            talk = {'hour': hour}
            for t in talkss:
                talk[t.room.name] = t.title
            talks.append(talk)

        table = klass(talks)
        tabless[talk_type.name] = table

    return render(request, "talks/schedule.html", {'tables': tabless})
