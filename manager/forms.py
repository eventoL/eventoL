# encoding: UTF-8
from django import forms
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

import autocomplete_light as autocomplete

autocomplete.autodiscover()

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


class AttendantAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name', 'surname', 'nickname', 'email')


class HardwareManufacturerAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name',)


class AttendantBySedeAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendant')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        sede_id = self.request.GET.get('sede_id', None)

        choices = []

        if sede_id:
            choices = self.choices.all()
            choices = choices.filter(sede__pk=sede_id)
            if q:
                choices = choices.filter(
                    Q(name__icontains=q) | Q(surname__icontains=q) | Q(
                        nickname__icontains=q) | Q(email__icontains=q))

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete.register(Attendant, AttendantAutocomplete)
autocomplete.register(HardwareManufacturer, HardwareManufacturerAutocomplete)
autocomplete.register(Attendant, AttendantBySedeAutocomplete)


def sorted_choices(choices_list):
    choices_list += [('', '-------------')]
    return sorted(set(choices_list))


class AttendantSearchForm(forms.Form):
    sedes = Sede.objects.distinct()
    sede = ChoiceField(
        label=_('Sede'),
        choices=sorted_choices([(sede.pk, sede.name) for sede in sedes])
    )
    attendant = autocomplete.ModelChoiceField('AttendantBySedeAutocomplete', required=False)


class RegistrationForm(DeferredForm):
    sedes = Sede.objects.distinct().prefetch_related('country')
    country = ChoiceField(
        label=_('Country'),
        choices=sorted_choices([(sede.country.code, sede.country.name) for sede in sedes]),
        required=False
    )
    state = CharField(label=_('State'), required=False, widget=widgets.Select())
    city = CharField(label=_('City'), required=False, widget=widgets.Select())

    def send_notification(self, instance=None):
        send_mail(_("FLISoL Registration Confirmation"),
                  render_to_string(
                      "mail/registration_confirmation.txt",
                      {'token': instance.token, 'form': self}
                  ),
                  'reyiyo@gmail.com',
                  recipient_list=[self.cleaned_data['email'], ],
                  fail_silently=False
        )

    class Meta:
        model = Attendant
        fields = ['name', 'surname', 'nickname', 'email', 'country', 'state',
                  'city', 'sede', 'is_going_to_install', 'additional_info']


class AttendantRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Attendant
        fields = ('name', 'surname', 'nickname', 'email', 'sede',
                  'is_going_to_install', 'additional_info')


class InstallationForm(autocomplete.ModelForm):
    class Meta:
        model = Installation
        exclude = ('installer', 'hardware')
        autocomplete_fields = ('attendant',)


class HardwareForm(autocomplete.ModelForm):
    class Meta:
        model = Hardware
        autocomplete_fields = ('manufacturer',)


class CollaboratorRegistrationForm(ModelForm):
    class Meta:
        model = Organizer
        exclude = ['user', 'is_coordinator', 'assisted']


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador'
    read_guidelines = forms.MultipleChoiceField(
        label='', required=True, widget=forms.CheckboxSelectMultiple,
        choices=((1, mark_safe(text)),)
    )

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
