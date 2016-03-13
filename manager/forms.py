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
    Installer, TalkProposal, HardwareManufacturer, ContactMessage, Image, Comment, Room, EventoLUser, Activity


class AttendeeAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('eventolUser__user__name', 'eventolUser__user__surname', 'eventolUser__user__nickname', 'eventolUser__user__email')


class HardwareManufacturerAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name',)


class AttendeeByEventAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendee')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        event_slug = self.request.GET.get('event_slug', None)

        choices = []

        if event_slug:
            choices = self.choices.all()
            choices = choices.filter(eventolUser__event__slug__iexact=event_slug)
            if q:
                choices = choices.filter(
                    Q(eventolUser__user__name__icontains=q) | Q(eventolUser__user__surname__icontains=q) | Q(
                        eventolUser__user__nickname__icontains=q) | Q(eventolUser__user__email__icontains=q))

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete.register(Attendee, AttendeeAutocomplete)
autocomplete.register(HardwareManufacturer, HardwareManufacturerAutocomplete)
autocomplete.register(Attendee, AttendeeByEventAutocomplete)


def sorted_choices(choices_list):
    choices_list += [('', '-------------')]
    return sorted(set(choices_list))


class AttendeeSearchForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(AttendeeSearchForm, self).__init__(*args, **kwargs)
        self.fields['attendee'].queryset = Attendee.objects.filter(eventolUser__event__slug=event)

    attendee = autocomplete.ModelChoiceField('AttendeeByEventAutocomplete', required=False)


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
                       'event_slug': self.cleaned_data['event'].url,
                       'domain': self.domain, 'protocol': self.protocol}),
                  EMAIL_FROM,
                  recipient_list=[self.cleaned_data['email'], ],
                  fail_silently=False)

    class Meta:
        model = Attendee
        fields = ['eventolUser', 'additional_info']
        widgets = {'eventolUser': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Attendee
        widgets = {'eventolUser': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class InstallationForm(autocomplete.ModelForm):
    def __init__(self, event, *args, **kwargs):
        super(InstallationForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['attendee'].queryset = Attendee.objects.filter(event__slug=event)

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
        widgets = {'eventolUser': forms.HiddenInput()}


class EventoLUserRegistrationForm(ModelForm):
    class Meta:
        model = EventoLUser
        exclude = ['user', 'assisted']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    class Meta:
        model = Attendee
        widgets = {'eventolUser': forms.HiddenInput()}


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        widgets = {'eventolUser': forms.HiddenInput()}


class InstallerRegistrationFromCollaboratorForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        fields = ['level']
        widgets = {'eventolUser': forms.HiddenInput()}


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
        exclude = ['confirmed_talk']
        widgets = {
            'image': forms.HiddenInput(),
            'activity': forms.HiddenInput()
        }


class ImageCroppingForm(ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'cropping')


class ActivityForm(ModelForm):
    def __init__(self, event, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['room'].queryset = Room.objects.filter(event__slug=event)
            self.fields['speakers'].queryset = EventoLUser.objects.filter(event__slug=event)

    class Meta:
        model = Activity
        widgets = {
            'event': forms.HiddenInput(),
            'long_description': forms.Textarea(attrs={'rows': 3}),
            'abstract': forms.Textarea(attrs={'rows': 3})
        }


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
        exclude = ["activity", "user"]
