# encoding: UTF-8
from dal import autocomplete
from django import forms
from django.core.validators import validate_email, URLValidator
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe

from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import SignupForm as AllAuthSignUpForm
from allauth.socialaccount.forms import SignupForm as AllAuthSocialSignUpForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import SetPasswordForm as AllAuthSetPasswordForm
from captcha.fields import ReCaptchaField

from manager.models import Attendee, Installation, \
    Hardware, Collaborator, Installer, ContactMessage, \
    EventUser, Event, Software, Contact, Activity


class SoftwareAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Software.objects.none()

        qs = Software.objects.all()

        if self.q:
            qs = qs.filter(name__unaccent__icontains=self.q)

        return qs[:5]


class AttendeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Attendee.objects.none()

        event_user = EventUser.objects.filter(user=self.request.user).first()

        qs = Attendee.objects.filter(event=event_user.event).filter(attended=False)

        if event_user and self.q:
            qs = qs.filter(
                Q(first_name__unaccent__icontains=self.q)
                | Q(last_name__unaccent__icontains=self.q)
                | Q(nickname__unaccent__icontains=self.q)
                | Q(email__icontains=self.q)
            )

        return qs[:5]


class EventUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return EventUser.objects.none()

        event_user = EventUser.objects.filter(user=self.request.user).first()

        qs = EventUser.objects.filter(event=event_user.event)

        if event_user and self.q:
            qs = qs.filter(
                Q(user__first_name__unaccent__icontains=self.q)
                | Q(user__last_name__unaccent__icontains=self.q)
                | Q(user__username__unaccent__icontains=self.q)
                | Q(user__email__icontains=self.q)
            )

        return qs[:5]


class AttendeeSearchForm(forms.Form):
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.all(),
        widget=autocomplete.ModelSelect2(url='attendee-autocomplete'),
        required=False,
        label=_("Attendee")
    )


class EventUserSearchForm(forms.Form):
    event_user = forms.ModelChoiceField(
        queryset=EventUser.objects.all(),
        widget=autocomplete.ModelSelect2(url='eventuser-autocomplete'),
        required=False,
        label=_("Collaborator/Installer")
    )


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email', 'additional_info', 'is_installing', 'event',
                  'attended', 'registration_date']
        widgets = {'event': forms.HiddenInput(), 'attended': forms.HiddenInput(),
                   'registration_date': forms.HiddenInput(), 'additional_info': forms.TextInput()}


class InstallationForm(forms.ModelForm):
    class Meta(object):
        model = Installation
        fields = ('attendee', 'notes', 'software')
        widgets = {'notes': forms.Textarea(attrs={'rows': 3}),
                   'attendee': autocomplete.ModelSelect2(url='attendee-autocomplete'),
                   'software': autocomplete.ModelSelect2(url='software-autocomplete')
                   }


class HardwareForm(forms.ModelForm):
    class Meta(object):
        model = Hardware
        fields = ('type', 'manufacturer', 'model')


class CollaboratorRegistrationForm(ModelForm):
    class Meta(object):
        model = Collaborator
        widgets = {'event_user': forms.HiddenInput()}
        exclude = ()


class EventUserRegistrationForm(ModelForm):
    class Meta(object):
        model = EventUser
        exclude = ['user', 'attended', 'ticket']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    repeat_email = forms.EmailField(label=_("Repeat Email"))
    captcha = ReCaptchaField(label=_("Are you a human?"))

    field_order = ['first_name', 'last_name', 'nickname', 'email', 'is_installing', 'repeat_email',
                   'additional_info', 'captcha', 'event',
                   'registration_date']

    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email', 'additional_info', 'is_installing', 'event',
                  'registration_date']
        widgets = {'event': forms.HiddenInput(), 'additional_info': forms.TextInput(),
                   'registration_date': forms.HiddenInput(), }

    def clean(self):
        cleaned_data = super(AttendeeRegistrationForm, self).clean()
        email = cleaned_data.get("email")
        repeat_email = cleaned_data.get("repeat_email")

        if email and repeat_email:
            if email != repeat_email:
                raise forms.ValidationError(
                    {'email': _("Emails do not match."), 'repeat_email': _("Emails do not match.")})

        return cleaned_data


class InstallerRegistrationForm(ModelForm):
    text = u'Afirmo que he leido la ' \
           u'"<a href="//wiki.cafelug.org.ar/index.php/Flisol/2016/Guía_del_' \
           u'buen_instalador" target="_blank">Sagrada Guía del Buen Instalador</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta(object):
        model = Installer
        widgets = {'event_user': forms.HiddenInput()}
        exclude = ()


class ImageCroppingForm(ModelForm):
    class Meta(object):
        model = Activity
        fields = ('image', 'cropping')


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


class ContactMessageForm(ModelForm):
    class Meta(object):
        model = ContactMessage
        fields = ('name', 'email', 'message',)
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


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


class ActivityProposalForm(ModelForm):
    repeat_email = forms.EmailField(label=_("Repeat Email"))
    captcha = ReCaptchaField(label=_("Are you a human?"))

    field_order = ['event', 'title', 'speakers_names', 'abstract', 'long_description', 'speaker_contact',
                   'repeat_email', 'labels', 'level', 'presentation', 'additional_info', 'status', 'captcha']

    def clean(self):
        cleaned_data = super(ActivityProposalForm, self).clean()
        email = cleaned_data.get("email")
        repeat_email = cleaned_data.get("repeat_email")

        if email and repeat_email:
            if email != repeat_email:
                raise forms.ValidationError(
                    {'email': _("Emails do not match."), 'repeat_email': _("Emails do not match.")})

        return cleaned_data

    class Meta(object):
        model = Activity
        fields = ['event', 'title', 'speakers_names', 'abstract', 'long_description', 'speaker_contact',
                  'labels', 'presentation', 'level', 'additional_info', 'status']
        widgets = {
            'event': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'abstract': forms.Textarea(attrs={'rows': 3}),
            'long_description': forms.Textarea(attrs={'rows': 3}),
            'additional_info': forms.Textarea(attrs={'rows': 3})
        }
