# encoding: UTF-8
from autocomplete_light import shortcuts as autocomplete
from django import forms
from django.core.validators import validate_email, URLValidator
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

autocomplete.autodiscover()

from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import SignupForm as AllAuthSignUpForm
from allauth.socialaccount.forms import SignupForm as AllAuthSocialSignUpForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import SetPasswordForm as AllAuthSetPasswordForm

from manager.models import Attendee, Installation, \
    Hardware, Collaborator, Installer, TalkProposal, ContactMessage, Image, \
    Comment, Room, EventUser, Activity, Event, Software, Contact


class SoftwareAutocomplete(autocomplete.AutocompleteModelBase):
    search_fields = ('name',)


class AttendeeAutocomplete(autocomplete.AutocompleteModelBase):
    autocomplete_js_attributes = {'placeholder': _('Search Attendee')}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        event_slug = self.request.GET.get('event_slug', None)

        choices = []
        if event_slug:
            choices = self.choices.all()
            choices = choices.filter(event__slug__iexact=event_slug).filter(attended=False)
            if q:
                choices = choices.filter(
                    Q(first_name__icontains=q)
                    | Q(last_name__icontains=q)
                    | Q(nickname__icontains=q)
                    | Q(email__icontains=q)
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
autocomplete.register(EventUser, RegisteredEventUserAutocomplete)
autocomplete.register(Software, SoftwareAutocomplete)


def sorted_choices(choices_list):
    choices_list += [('', '-------------')]
    return sorted(set(choices_list))


class AttendeeSearchForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(AttendeeSearchForm, self).__init__(*args, **kwargs)
        # Los EventUser para el evento que todavia no registraron asistencia
        self.fields['attendee'].queryset = Attendee.objects.filter(event__slug__iexact=event).filter(attended=False)

    attendee = autocomplete.ModelChoiceField('AttendeeAutocomplete', required=False)


class RegisteredEventUserSearchForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(RegisteredEventUserSearchForm, self).__init__(*args, **kwargs)
        self.fields['eventUser'].queryset = EventUser.objects.filter(event__slug__iexact=event)

    eventUser = autocomplete.ModelChoiceField('EventUserRegisteredEventUserAutocomplete', required=False)


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email', 'additional_info', 'is_installing', 'event',
                  'attended', 'registration_date']
        widgets = {'event': forms.HiddenInput(), 'attended': forms.HiddenInput(),
                   'registration_date': forms.HiddenInput(), 'additional_info': forms.TextInput()}


class InstallationForm(autocomplete.ModelForm):
    def __init__(self, event, *args, **kwargs):
        super(InstallationForm, self).__init__(*args, **kwargs)
        self.fields['attendee'].queryset = Attendee.objects.filter(event__slug__iexact=event)

    attendee = autocomplete.ModelChoiceField('AttendeeAutocomplete', required=True)

    class Meta(object):
        model = Installation
        fields = ('attendee', 'notes', 'software')
        autocomplete_fields = ('attendee', 'software')
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}


class HardwareForm(autocomplete.ModelForm):
    class Meta(object):
        model = Hardware
        fields = ('type', 'manufacturer', 'model')


class CollaboratorRegistrationForm(ModelForm):
    class Meta(object):
        model = Collaborator
        widgets = {'eventUser': forms.HiddenInput()}
        exclude = ()


class EventUserRegistrationForm(ModelForm):
    class Meta(object):
        model = EventUser
        exclude = ['user', 'attended', 'ticket']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email', 'additional_info', 'is_installing', 'event',
                  'registration_date']
        widgets = {'event': forms.HiddenInput(), 'additional_info': forms.TextInput(),
                   'registration_date': forms.HiddenInput(), }


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2016/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta(object):
        model = Installer
        widgets = {'eventUser': forms.HiddenInput()}
        exclude = ()


class TalkProposalForm(ModelForm):
    class Meta(object):
        model = TalkProposal
        exclude = ['confirmed_talk']
        widgets = {
            'image': forms.HiddenInput(),
            'activity': forms.HiddenInput()
        }


class TalkForm(ModelForm):
    class Meta(object):
        model = Activity
        fields = ['start_date', 'end_date', 'room', 'event']
        widgets = {
            'event': forms.HiddenInput()
        }

    def __init__(self, event, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['room'].queryset = Room.objects.filter(event__slug__iexact=event)


class ImageCroppingForm(ModelForm):
    class Meta(object):
        model = Image
        fields = ('image', 'cropping')


class RoomForm(ModelForm):
    class Meta(object):
        model = Room
        exclude = ['event']


class ContactForm(ModelForm):
    class Meta(object):
        model = Contact
        exclude = ['event']

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        type = cleaned_data.get("type")
        value = cleaned_data.get("url")

        if type:
            if type.validate == '1':
                try:
                    validator = URLValidator()
                    validator(value)
                except Exception:
                    self.add_error('url', 'Enter valid URL')

            elif type.validate == '2':
                try:
                    validate_email(value)
                except Exception:
                    self.add_error('url', 'Enter valid Email')
        else:  # type none
            self.add_error('type', _('This field is required'))

        return cleaned_data


class ActivityForm(ModelForm):
    class Meta(object):
        model = Activity
        exclude = ['confirmed', 'room', 'start_date', 'end_date']
        widgets = {
            'event': forms.HiddenInput(),
            'long_description': forms.Textarea(attrs={'rows': 3}),
            'abstract': forms.Textarea(attrs={'rows': 3})
        }


class ActivityAdminForm(ModelForm):
    def clean(self):
        obj = self.instance
        if obj.start_date or obj.end_date:
            Activity.room_available(error=True, instance=obj, event_slug=obj.event.slug)


class ActivityCompleteForm(ModelForm):
    class Meta(object):
        model = Activity
        exclude = ['confirmed']
        widgets = {
            'event': forms.HiddenInput(),
            'long_description': forms.Textarea(attrs={'rows': 3}),
            'abstract': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, event_slug, *args, **kwargs):
        super(ActivityCompleteForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['room'].queryset = Room.objects.filter(event__slug__iexact=event_slug)


class PresentationForm(ModelForm):
    class Meta(object):
        model = TalkProposal
        fields = ('presentation',)


class ContactMessageForm(ModelForm):
    class Meta(object):
        model = ContactMessage
        fields = ('name', 'email', 'message',)
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class CommentForm(ModelForm):
    class Meta(object):
        model = Comment
        exclude = ["activity", "user"]


class EventForm(ModelForm):
    class Meta(object):
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
