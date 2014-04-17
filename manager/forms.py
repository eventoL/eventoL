# encoding: UTF-8
import autocomplete_light
from django import forms
autocomplete_light.autodiscover()
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import widgets
from django.forms.fields import ChoiceField, CharField
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from generic_confirmation.forms import DeferredForm

from manager.models import Attendant, Installation, Hardware, Organizer, \
    Installer, Sede, TalkProposal, HardwareManufacturer


class AttendantAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('name', 'surname', 'nickname', 'email')


class HardwareManufacturerAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('name',)


autocomplete_light.register(Attendant, AttendantAutocomplete)
autocomplete_light.register(HardwareManufacturer, HardwareManufacturerAutocomplete)


class AttendantSearchByCollaboratorForm(forms.Form):
    attendant = autocomplete_light.ModelChoiceField('AttendantAutocomplete')


class RegistrationForm(DeferredForm):
    country = ChoiceField(label=_('Country'), choices=sorted(set([(sede.country.code, sede.country.name) for sede in Sede.objects.distinct().prefetch_related('country')] + [('', '-------------')])), required=False)
    state = CharField(label=_('State'), required=False, widget=widgets.Select())
    city = CharField(label=_('City'), required=False, widget=widgets.Select())

    def send_notification(self, user=None, instance=None):
        send_mail(_("FLISoL Registration Confirmation"),
            render_to_string("mail/registration_confirmation.txt", {'token': instance.token, 'form': self}),
            'reyiyo@gmail.com',
            recipient_list=[self.cleaned_data['email'], ], fail_silently=False)

    class Meta:
        model = Attendant
        fields = ['name', 'surname', 'nickname', 'email', 'country', 'state', 'city', 'sede', 'is_going_to_install', 'additional_info']


class InstallationForm(autocomplete_light.ModelForm):

    class Meta:
        model = Installation
        exclude = ('installer', 'hardware')
        autocomplete_fields = ('attendant',)


class HardwareForm(autocomplete_light.ModelForm):

    class Meta:
        model = Hardware
        autocomplete_fields = ('manufacturer',)


class CollaboratorRegistrationForm(ModelForm):

    class Meta:
        model = Organizer
        exclude = ['user', 'is_coordinator', 'assisted']


class InstallerRegistrationForm(ModelForm):

    class Meta:
        model = Installer
        exclude = ['user', 'is_coordinator', 'assisted']


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
        exclude = ('cropping',)


class TalkProposalImageCroppingForm(ModelForm):

    class Meta:
        model = TalkProposal
        fields = ('home_image', 'cropping',)
