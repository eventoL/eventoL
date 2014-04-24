# encoding: UTF-8
import autocomplete_light
from django import forms
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe
autocomplete_light.autodiscover()
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import widgets
from django.forms.fields import ChoiceField, CharField, BooleanField, \
    MultipleChoiceField
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


class AttendantBySedeAutocomplete(autocomplete_light.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendant')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        sede_id = self.request.GET.get('sede_id', None)

        choices = []

        if sede_id:
            choices = self.choices.all()
            choices = choices.filter(sede__pk=sede_id)
            if q:
                choices = choices.filter(Q(name__icontains=q) | Q(surname__icontains=q) | Q(nickname__icontains=q) | Q(email__icontains=q))

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Attendant, AttendantAutocomplete)
autocomplete_light.register(HardwareManufacturer, HardwareManufacturerAutocomplete)
autocomplete_light.register(Attendant, AttendantBySedeAutocomplete)

class AttendantSearchForm(forms.Form):

    sede = ChoiceField(label=_('Sede'), choices=sorted(set([(sede.pk, sede.name) for sede in Sede.objects.distinct()] + [('', '-------------')])))
    attendant = autocomplete_light.ModelChoiceField('AttendantBySedeAutocomplete', required=False)


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


class AttendantRegistrationByCollaboratorForm(forms.ModelForm):

    class Meta:
        model = Attendant
        fields = ('name', 'surname', 'nickname', 'email', 'sede', 'is_going_to_install', 'additional_info')

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
    
    read_guidelines = forms.MultipleChoiceField(label='', required=True,
        widget=forms.CheckboxSelectMultiple, 
        choices=((1, mark_safe(u'Afirmo que he leido la <a href="//wiki.cafelug.org.ar/index.php/Flisol/2014/Guía_del_buen_instalador" target="_blank">Sagrada Guía del Buen Instalador')),)) 
    
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
