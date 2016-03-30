# encoding: UTF-8
import autocomplete_light as autocomplete
from django import forms
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

autocomplete.autodiscover()

from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from generic_confirmation.forms import DeferredForm
from eventoL.settings import EMAIL_FROM
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import SignupForm as AllAuthSignUpForm
from allauth.socialaccount.forms import SignupForm as AllAuthSocialSignUpForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import SetPasswordForm as AllAuthSetPasswordForm

from manager.models import Attendee, InstallationAttendee, NonRegisteredAttendee, Installation, Hardware, \
    Collaborator, \
    Installer, TalkProposal, HardwareManufacturer, ContactMessage, Image, Comment, Room, EventUser, Activity, Event


class AttendeeAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('eventUser__user__first_name', 'eventUser__user__last_name', 'eventUser__user__username',
                     'eventUser__user__email')


class HardwareManufacturerAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name',)


class EventUserAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendee')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        event_slug = self.request.GET.get('event_slug', None)

        choices = []
        if event_slug:
            choices = self.choices.all()
            choices = choices.filter(event__slug__iexact=event_slug).filter(assisted=False)
            if q:
                choices = choices.filter(
                    Q(user__first_name__icontains=q)
                    | Q(user__last_name__icontains=q)
                    | Q(user__username__icontains=q)
                    | Q(user__email__icontains=q)
                    | Q(nonregisteredattendee__first_name__icontains=q)
                    | Q(nonregisteredattendee__last_name__icontains=q)
                    | Q(nonregisteredattendee__email__icontains=q)
                )

        return self.order_choices(choices)[0:self.limit_choices]


class RegisteredEventUserAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Type to search'),
                                  'label': _('User')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        event_slug = self.request.GET.get('event_slug', None)

        choices = []
        if event_slug:
            choices = self.choices.all()
            choices = choices.filter(event__slug__iexact=event_slug)
            if q:
                choices = choices.filter(
                    Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(
                        user__username__icontains=q) | Q(user__email__icontains=q)
                )

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete.register(Attendee, AttendeeAutocomplete)
autocomplete.register(HardwareManufacturer, HardwareManufacturerAutocomplete)
autocomplete.register(EventUser, EventUserAutocomplete)
autocomplete.register(EventUser, RegisteredEventUserAutocomplete)


def sorted_choices(choices_list):
    choices_list += [('', '-------------')]
    return sorted(set(choices_list))


class EventUserSearchForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(EventUserSearchForm, self).__init__(*args, **kwargs)
        # Los EventUser para el evento que todavia no registraron asistencia
        self.fields['eventUser'].queryset = EventUser.objects.filter(event__slug=event).filter(assisted=False)

    eventUser = autocomplete.ModelChoiceField('EventUserAutocomplete', required=False)


class RegisteredEventUserSearchForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(RegisteredEventUserSearchForm, self).__init__(*args, **kwargs)
        self.fields['eventUser'].queryset = EventUser.objects.filter(event__slug=event)

    eventUser = autocomplete.ModelChoiceField('EventUserRegisteredEventUserAutocomplete', required=False)


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
        model = NonRegisteredAttendee
        fields = ['first_name', 'last_name', 'email', 'installation_additional_info', 'is_installing']
        widgets = {'event': forms.HiddenInput(), 'assisted': forms.HiddenInput(),
                   'installation_additional_info': forms.TextInput()}


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
        exclude = ['user', 'assisted', 'nonregisteredattendee']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    is_installing = forms.BooleanField(label=_('Bringing a device for installation?'), required=False)
    installation_additional_info = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), help_text=_(
        'i.e. Wath kind of PC are you bringing? Leave blank if doesn\'t apply'), required=False)

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


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = self.fields['login'].widget.attrs['placeholder']
        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']


class SignUpForm(AllAuthSignUpForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in ['username', 'email', 'password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ResetPasswordForm(AllAuthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for field in ['email']:
            del self.fields[field].widget.attrs['placeholder']


class ResetPasswordKeyForm(AllAuthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class ChangePasswordForm(AllAuthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field in ['oldpassword', 'password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class SetPasswordForm(AllAuthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class SocialSignUpForm(AllAuthSocialSignUpForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))

    def __init__(self, *args, **kwargs):
        super(SocialSignUpForm, self).__init__(*args, **kwargs)
        for field in ['username', 'email']:
            del self.fields[field].widget.attrs['placeholder']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
