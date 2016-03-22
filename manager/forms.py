# encoding: UTF-8
import autocomplete_light as autocomplete
from django import forms
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

autocomplete.autodiscover()

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from generic_confirmation.forms import DeferredForm
from eventoL.settings import EMAIL_FROM

from manager.models import Attendee, InstallationAttendee, Installation, Hardware, Collaborator, \
    Installer, TalkProposal, HardwareManufacturer, ContactMessage, Image, Comment, Room, EventUser, Activity, Event


class AttendeeAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('eventUser__user__first_name', 'eventUser__user__last_name', 'eventUser__user__username',
                     'eventUser__user__email')


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
            choices = choices.filter(eventUser__event__slug__iexact=event_slug)
            if q:
                choices = choices.filter(
                    Q(eventUser__user__first_name__icontains=q) | Q(eventUser__user__last_name__icontains=q) | Q(
                        eventUser__user__username__icontains=q) | Q(eventUser__user__email__icontains=q))

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
        self.fields['attendee'].queryset = Attendee.objects.filter(eventUser__event__slug=event)

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
        fields = ['eventUser', 'additional_info']
        widgets = {'eventUser': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Attendee
        widgets = {'eventUser': forms.HiddenInput(),
                   'additional_info': forms.Textarea(attrs={'rows': 3})}


class InstallationForm(autocomplete.ModelForm):
    def __init__(self, event, *args, **kwargs):
        super(InstallationForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['attendee'].queryset = InstallationAttendee.objects.filter(eventUser__event__slug=event)

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
        widgets = {'eventUser': forms.HiddenInput()}


class EventUserRegistrationForm(ModelForm):
    class Meta:
        model = EventUser
        exclude = ['user', 'assisted']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    class Meta:
        model = Attendee
        widgets = {'eventUser': forms.HiddenInput()}


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2016/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        widgets = {'eventUser': forms.HiddenInput()}


class InstallerRegistrationFromCollaboratorForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2016/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        fields = ['level']
        widgets = {'eventUser': forms.HiddenInput()}


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


class TalkForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['start_date', 'end_date', 'room', 'confirmed', 'event']
        widgets = {
            'event': forms.HiddenInput()
        }

    def __init__(self, event, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['room'].queryset = Room.objects.filter(event__slug=event)


class ImageCroppingForm(ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'cropping')


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['confirmed', 'room', 'start_date', 'end_date']
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
        fields = ('name', 'email', 'message',)
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["activity", "user"]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'slug', 'date', 'limit_proposal_date', 'email', 'place', 'external_url', 'event_information')
        widgets = {'date': forms.HiddenInput(),
                   'place': forms.HiddenInput(),
                   'limit_proposal_date': forms.HiddenInput()}
