# encoding: UTF-8
from django import forms
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

import autocomplete_light as autocomplete

autocomplete.autodiscover()

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from generic_confirmation.forms import DeferredForm
from eventoL.settings import EMAIL_FROM

from manager.models import Attendee, Installation, Hardware, Collaborator, \
    Installer, TalkProposal, HardwareManufacturer, ContactMessage, Talk, Comment, Room


class AttendeeAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name', 'surname', 'nickname', 'email')


class HardwareManufacturerAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name',)


class AttendeeBySedeAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendee')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        sede_url = self.request.GET.get('sede_url', None)

        choices = []

        if sede_url:
            choices = self.choices.all()
            choices = choices.filter(sede__url__iexact=sede_url)
            if q:
                choices = choices.filter(
                    Q(name__icontains=q) | Q(surname__icontains=q) | Q(
                        nickname__icontains=q) | Q(email__icontains=q))

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete.register(Attendee, AttendeeAutocomplete)
autocomplete.register(HardwareManufacturer, HardwareManufacturerAutocomplete)
autocomplete.register(Attendee, AttendeeBySedeAutocomplete)


def sorted_choices(choices_list):
    choices_list += [('', '-------------')]
    return sorted(set(choices_list))


class AttendeeSearchForm(forms.Form):
    def __init__(self, sede, *args, **kwargs):
        super(AttendeeSearchForm, self).__init__(*args, **kwargs)
        self.fields['attendee'].queryset = Attendee.objects.filter(sede__url=sede)

    attendee = autocomplete.ModelChoiceField('AttendeeBySedeAutocomplete', required=False)


class RegistrationForm(DeferredForm):
    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop('domain', None)
        self.protocol = kwargs.pop('protocol', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def send_notification(self, user=None, instance=None):
        send_mail(_("FLISoL Registration Confirmation"),
                  render_to_string(
                      "mail/registration_confirmation.txt",
                      {'token': instance.token, 'form': self,
                       'sede_url': self.cleaned_data['sede'].url,
                       'domain': self.domain, 'protocol': self.protocol}),
                  EMAIL_FROM,
                  recipient_list=[self.cleaned_data['email'], ],
                  fail_silently=False)

    class Meta:
        model = Attendee
        fields = ['name', 'surname', 'nickname', 'email', 'sede', 'is_going_to_install', 'additional_info']
        widgets = {'sede': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ('name', 'surname', 'nickname', 'email', 'sede',
                  'is_going_to_install', 'additional_info')
        widgets = {'sede': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class InstallationForm(autocomplete.ModelForm):
    def __init__(self, sede, *args, **kwargs):
        super(InstallationForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['attendee'].queryset = Attendee.objects.filter(sede__url=sede)

    class Meta:
        model = Installation
        exclude = ('installer', 'hardware')
        autocomplete_fields = ('attendee',)


class HardwareForm(autocomplete.ModelForm):
    class Meta:
        model = Hardware
        autocomplete_fields = ('manufacturer',)


class CollaboratorRegistrationForm(ModelForm):
    class Meta:
        model = Collaborator
        exclude = ['user', 'is_coordinator', 'assisted']
        widgets = {'sede': forms.HiddenInput()}


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        exclude = ['user', 'is_coordinator', 'assisted', 'collaborator']
        widgets = {'sede': forms.HiddenInput()}


class InstallerRegistrationFromCollaboratorForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        fields = ['level', 'software']
        widgets = {'sede': forms.HiddenInput()}


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class TalkProposalForm(ModelForm):
    class Meta:
        model = TalkProposal
        exclude = ('cropping', 'confirmed', 'dummy_talk')
        widgets = {'sede': forms.HiddenInput(),
                   'long_description': forms.Textarea(attrs={'rows': 3}),
                   'abstract': forms.Textarea(attrs={'rows': 3})}


class TalkProposalImageCroppingForm(ModelForm):
    class Meta:
        model = TalkProposal
        fields = ('home_image', 'cropping')


class TalkForm(ModelForm):
    def __init__(self, sede, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['room'].queryset = Room.objects.filter(sede__url=sede)
            self.fields['speakers'].queryset = Collaborator.objects.filter(sede__url=sede)

    class Meta:
        model = Talk
        exclude = ('talk_proposal',)


class PresentationForm(ModelForm):

    class Meta:
        model = TalkProposal
        fields = ('presentation',)


class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message', )
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["proposal", "user"]
