# pylint: disable=too-many-ancestors

import datetime
import logging

from collections import OrderedDict
from captcha.fields import CaptchaField
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.utils.formats import date_format
from django.core.validators import validate_email, URLValidator
from django.db.models.query_utils import Q
from django.db.utils import OperationalError
from django.forms.models import ModelForm, BaseModelFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from manager.models import (Attendee, Installation, Hardware, Collaborator,
                            Installer, ContactMessage, EventUser, Event,
                            Software, Contact, Activity, EventDate, Room,
                            AttendeeAttendanceDate, EventUserAttendanceDate)

from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import SignupForm as AllAuthSignUpForm
from allauth.socialaccount.forms import SignupForm as AllAuthSocialSignUpForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm \
    as AllAuthResetPasswordKeyForm
from allauth.account.forms import ChangePasswordForm \
    as AllAuthChangePasswordForm
from allauth.account.forms import SetPasswordForm as AllAuthSetPasswordForm


logger = logging.getLogger('eventol')


class GenericAutocomplete(autocomplete.Select2QuerySetView):
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except OperationalError as error:
            logger.error(error)
            self.use_unaccent = False
            return super().get(request, *args, **kwargs)


class SoftwareAutocomplete(GenericAutocomplete):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Software.objects.none()
        softwares = Software.objects.all()
        if self.q:
            if not hasattr(self, 'use_unaccent') or self.use_unaccent:
                softwares = softwares.filter(name__unaccent__icontains=self.q)
            else:
                softwares = softwares.filter(name__icontains=self.q)
        return softwares[:5]


class AttendeeAutocomplete(GenericAutocomplete):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Attendee.objects.none()
        event_uid = self.forwarded.get('event_uid', None)
        event_user = EventUser.objects.filter(
            user=self.request.user, event__uid=event_uid).first()

        attended = [attendance_date.attendee.pk for attendance_date in
                    AttendeeAttendanceDate.objects.filter(
                        attendee__event__uid=event_uid,
                        date__date=datetime.date.today())]

        attendees = Attendee.objects \
            .filter(event__uid=event_uid).exclude(pk__in=attended)

        if event_user and self.q:
            if not hasattr(self, 'use_unaccent') or self.use_unaccent:
                attendees = attendees.filter(
                    Q(first_name__unaccent__icontains=self.q) |
                    Q(last_name__unaccent__icontains=self.q) |
                    Q(nickname__unaccent__icontains=self.q) |
                    Q(email__icontains=self.q)
                )
            else:
                attendees = attendees.filter(
                    Q(first_name__icontains=self.q) |
                    Q(last_name__icontains=self.q) |
                    Q(nickname__icontains=self.q) |
                    Q(email__icontains=self.q)
                )

        return attendees[:5]


class AllAttendeeAutocomplete(GenericAutocomplete):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Attendee.objects.none()
        event_uid = self.forwarded.get('event_uid', None)
        event_user = EventUser.objects.filter(
            user=self.request.user, event__uid=event_uid).first()
        attendees = Attendee.objects.filter(event__uid=event_uid)
        if event_user and self.q:
            if not hasattr(self, 'use_unaccent') or self.use_unaccent:
                attendees = attendees.filter(
                    Q(first_name__unaccent__icontains=self.q) |
                    Q(last_name__unaccent__icontains=self.q) |
                    Q(nickname__unaccent__icontains=self.q) |
                    Q(email__icontains=self.q)
                )
            else:
                attendees = attendees.filter(
                    Q(first_name__icontains=self.q) |
                    Q(last_name__icontains=self.q) |
                    Q(nickname__icontains=self.q) |
                    Q(email__icontains=self.q)
                )
        return attendees[:5]


class EventUserAutocomplete(GenericAutocomplete):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return EventUser.objects.none()

        event_uid = self.forwarded.get('event_uid', None)
        event_user = EventUser.objects.filter(
            user=self.request.user, event__uid=event_uid).first()

        attended = [attendance_date.event_user.pk for attendance_date in
                    EventUserAttendanceDate.objects.filter(
                        event_user__event__uid=event_uid,
                        date__date=datetime.date.today())]

        event_users = EventUser.objects \
            .filter(event=event_user.event).exclude(pk__in=attended)

        if event_user and self.q:
            if not hasattr(self, 'use_unaccent') or self.use_unaccent:
                event_users = event_users.filter(
                    Q(user__first_name__unaccent__icontains=self.q) |
                    Q(user__last_name__unaccent__icontains=self.q) |
                    Q(user__username__unaccent__icontains=self.q) |
                    Q(user__email__icontains=self.q)
                )
            else:
                event_users = event_users.filter(
                    Q(user__first_name__icontains=self.q) |
                    Q(user__last_name__icontains=self.q) |
                    Q(user__username__icontains=self.q) |
                    Q(user__email__icontains=self.q)
                )

        return event_users[:5]


class AttendeeSearchForm(forms.Form):
    def __init__(self, event_uid, *args, **kwargs):
        kwargs.update(initial={
            'event_uid': event_uid,
        })

        super().__init__(*args, **kwargs)
        self.fields['event_uid'].widget = forms.HiddenInput()

    event_uid = forms.UUIDField()
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='attendee-autocomplete', forward=['event_uid']),
        required=False,
        label=_("Attendee")
    )


class EventUserSearchForm(forms.Form):
    def __init__(self, event_uid, *args, **kwargs):
        kwargs.update(initial={
            'event_uid': event_uid,
        })
        super().__init__(*args, **kwargs)
        self.fields['event_uid'].widget = forms.HiddenInput()

    event_uid = forms.UUIDField()
    event_user = forms.ModelChoiceField(
        queryset=EventUser.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='eventuser-autocomplete', forward=['event_uid']),
        required=False,
        label=_("Collaborator/Installer")
    )


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email',
                  'additional_info', 'is_installing',
                  'event', 'registration_date']
        widgets = {'event': forms.HiddenInput(),
                   'registration_date': forms.HiddenInput(),
                   'additional_info': forms.TextInput()}


class InstallationForm(forms.ModelForm):
    def __init__(self, event_uid, *args, **kwargs):
        kwargs.update(initial={
            'event_uid': event_uid,
        })

        super().__init__(*args, **kwargs)
        self.fields['event_uid'].widget = forms.HiddenInput()

    event_uid = forms.UUIDField()

    class Meta(object):
        model = Installation
        fields = ('attendee', 'notes', 'software')
        widgets = {'notes': forms.Textarea(attrs={'rows': 3}),
                   'attendee': autocomplete.ModelSelect2(
                       url='all-attendee-autocomplete', forward=['event_uid']),
                   'software': autocomplete.ModelSelect2(
                       url='software-autocomplete')}


class HardwareForm(forms.ModelForm):
    class Meta(object):
        model = Hardware
        fields = ('type', 'manufacturer', 'model')


class ActivityForm(ModelForm):
    class Meta(object):
        model = Activity
        fields = ['start_date', 'end_date', 'room', 'event']
        widgets = {
            'event': forms.HiddenInput()
        }

    def __init__(self, event_slug, event_uid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            choices = []
            event_dates = EventDate.objects.filter(event__uid=event_uid)
            for event_date in event_dates:
                date_value = date_format(event_date.date, format='SHORT_DATE_FORMAT', use_l10n=True)
                choices.append((event_date.id, date_value,))
            self.fields['room'].queryset = Room.objects.filter(event__uid=event_uid)
            self.fields['date'] = forms.ChoiceField(choices=choices)


class CollaboratorRegistrationForm(ModelForm):
    class Meta(object):
        model = Collaborator
        widgets = {'event_user': forms.HiddenInput()}
        exclude = ()


class AttendeeRegistrationFromUserForm(ModelForm):
    field_order = ['first_name', 'last_name', 'nickname', 'additional_info',
                   'is_installing', 'email', 'event', 'event_user', 'registration_date']

    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email',
                  'additional_info', 'is_installing',
                  'event', 'registration_date', 'event_user']
        widgets = {'first_name': forms.HiddenInput(),
                   'last_name': forms.HiddenInput(),
                   'nickname': forms.HiddenInput(),
                   'event': forms.HiddenInput(),
                   'email': forms.HiddenInput(),
                   'event_user': forms.HiddenInput(),
                   'additional_info': forms.TextInput(),
                   'registration_date': forms.HiddenInput(), }


class EventUserRegistrationForm(ModelForm):
    class Meta(object):
        model = EventUser
        exclude = ['user', 'ticket']
        widgets = {'event': forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    repeat_email = forms.EmailField(label=_("Repeat Email"))
    captcha = CaptchaField()

    field_order = ['first_name', 'last_name', 'nickname', 'additional_info',
                   'is_installing', 'email', 'repeat_email', 'captcha',
                   'event', 'registration_date']

    class Meta(object):
        model = Attendee
        fields = ['first_name', 'last_name', 'nickname', 'email',
                  'additional_info', 'is_installing',
                  'event', 'registration_date']
        widgets = {'event': forms.HiddenInput(),
                   'additional_info': forms.TextInput(),
                   'registration_date': forms.HiddenInput(), }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        repeat_email = cleaned_data.get("repeat_email")

        if email and repeat_email:
            if email != repeat_email:
                raise forms.ValidationError({
                    'email': _("Emails do not match."),
                    'repeat_email': _("Emails do not match.")})

        return cleaned_data


class InstallerRegistrationForm(ModelForm):
    protocol = 'https://'
    url = 'wiki.cafelug.org.ar/index.php?title=Flisol/Guía_del_buen_instalador'
    target = '_blank'
    link_text = 'Sagrada Guía del Buen Instalador'
    text = 'Afirmo que he leido la "<a href="{0}{1}" target="{2}">{3}</a>"' \
        .format(protocol, url, target, link_text)
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta(object):
        model = Installer
        widgets = {'event_user': forms.HiddenInput()}
        exclude = ()


class ImageCroppingForm(ModelForm):
    class Meta(object):
        model = Activity
        fields = ('image', 'cropping')


class EventImageCroppingForm(ModelForm):
    class Meta(object):
        model = Event
        fields = ('image', 'cropping')


class ContactForm(ModelForm):
    class Meta(object):
        model = Contact
        exclude = ['event']

    def clean(self):
        cleaned_data = super().clean()
        data_type = cleaned_data.get("type")
        value = cleaned_data.get("url")

        if data_type:
            if data_type.validate == '1':
                try:
                    validator = URLValidator()
                    validator(value)
                except ValidationError:
                    self.add_error('url', 'Enter valid URL')

            elif data_type.validate == '2':
                try:
                    validate_email(value)
                except ValidationError:
                    self.add_error('url', 'Enter valid Email')
        else:  # data_type none
            self.add_error('type', _('This field is required'))
        return cleaned_data


class ContactMessageForm(ModelForm):
    class Meta(object):
        model = ContactMessage
        fields = ('name', 'email', 'message',)
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class EventDateForm(ModelForm):
    class Meta(object):
        model = EventDate
        fields = ('date',)


class EventDateModelFormset(BaseModelFormSet):

    @staticmethod
    def validate_date(date, dates):
        if date in dates:
            raise forms.ValidationError(
                _('One or more dates of the event are the same date'),
                code='duplicate_date'
            )

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        dates = []

        for form in self.forms:
            if form.cleaned_data:
                date = form.cleaned_data['date']
                if date:
                    self.validate_date(date, dates)
                    dates.append(date)


class EventForm(ModelForm):
    class Meta(object):
        model = Event
        fields = ('name', 'slug', 'limit_proposal_date', 'email',
                  'place', 'external_url', 'abstract', 'event_information')
        widgets = {'place': forms.HiddenInput(),
                   'limit_proposal_date': forms.HiddenInput()}


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = self.fields['login'].widget.attrs['placeholder']
        self.fields['login'].label = label
        del self.fields['login'].widget.attrs['placeholder']
        del self.fields['password'].widget.attrs['placeholder']


class SignUpForm(AllAuthSignUpForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))

    ordered_field_names = ['first_name', 'last_name', 'password1',
                           'password2', 'email', 'email2', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'email2', 'password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']

        original_fields = self.fields
        new_fields = OrderedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        for field in self.fields.keys():
            if field not in self.ordered_field_names:
                new_fields[field] = original_fields.get(field)

        self.fields = new_fields

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ResetPasswordForm(AllAuthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['email']:
            del self.fields[field].widget.attrs['placeholder']


class ResetPasswordKeyForm(AllAuthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class ChangePasswordForm(AllAuthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['oldpassword', 'password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class SetPasswordForm(AllAuthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            del self.fields[field].widget.attrs['placeholder']


class SocialSignUpForm(AllAuthSocialSignUpForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))

    ordered_field_names = ['email', 'email2', 'first_name',
                           'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'email2']:
            del self.fields[field].widget.attrs['placeholder']

        original_fields = self.fields
        new_fields = OrderedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        for field in self.fields.keys():
            if field not in self.ordered_field_names:
                new_fields[field] = original_fields.get(field)

        self.fields = new_fields

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ActivityProposalForm(ModelForm):
    repeat_email = forms.EmailField(label=_("Repeat Email"))
    captcha = CaptchaField(label=_("Are you a human?"))

    field_order = ['event', 'title', 'speakers_names', 'abstract',
                   'long_description', 'speaker_contact', 'repeat_email',
                   'labels', 'level', 'type', 'presentation',
                   'additional_info', 'captcha', 'status']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        repeat_email = cleaned_data.get("repeat_email")

        if email and repeat_email:
            if email != repeat_email:
                raise forms.ValidationError({
                    'email': _("Emails do not match."),
                    'repeat_email': _("Emails do not match.")})

        return cleaned_data

    class Meta(object):
        model = Activity
        fields = ['event', 'title', 'speakers_names', 'abstract',
                  'long_description', 'speaker_contact',
                  'labels', 'presentation', 'level',
                  'additional_info', 'status', 'type']
        widgets = {
            'event': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'abstract': forms.Textarea(attrs={'rows': 3}),
            'long_description': forms.Textarea(attrs={'rows': 3}),
            'additional_info': forms.Textarea(attrs={'rows': 3})
        }
