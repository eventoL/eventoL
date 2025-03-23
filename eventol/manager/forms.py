# pylint: disable=too-many-ancestors

import datetime
import logging
import uuid
from collections import OrderedDict

from allauth.account.forms import ChangePasswordForm as AllAuthChangePasswordForm
from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllAuthResetPasswordKeyForm
from allauth.account.forms import SetPasswordForm as AllAuthSetPasswordForm
from allauth.account.forms import SignupForm as AllAuthSignUpForm
from allauth.socialaccount.forms import SignupForm as AllAuthSocialSignUpForm
from captcha.fields import CaptchaField
from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db.models.query_utils import Q
from django.forms import Form
from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.models import BaseModelFormSet
from django.forms.models import ModelForm
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from image_cropping import ImageCropWidget
from tempus_dominus.widgets import DatePicker
from tempus_dominus.widgets import TimePicker

from manager.models import Activity
from manager.models import Attendee
from manager.models import AttendeeAttendanceDate
from manager.models import Collaborator
from manager.models import Contact
from manager.models import ContactMessage
from manager.models import Event
from manager.models import EventDate
from manager.models import EventUser
from manager.models import EventUserAttendanceDate
from manager.models import Hardware
from manager.models import Installation
from manager.models import Installer
from manager.models import Room
from manager.models import Software
from manager.utils.forms import USE_POSTGRES

logger = logging.getLogger("eventol")


class SoftwareAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Software.objects.none()
        softwares = Software.objects.all()
        softwares = softwares.filter(name__unaccent__icontains=self.q) if USE_POSTGRES else softwares.filter(name__icontains=self.q.lower())
        return softwares[:5]


class AttendeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Attendee.objects.none()
        event_slug = self.forwarded.get("event_slug", None)
        event_user = EventUser.objects.filter(user=self.request.user, event__event_slug=event_slug).first()

        attended = [
            attendance_date.attendee.pk
            for attendance_date in AttendeeAttendanceDate.objects.filter(attendee__event__event_slug=event_slug, date__date=datetime.date.today())
        ]

        attendees = Attendee.objects.filter(event__event_slug=event_slug).exclude(pk__in=attended)

        if event_user and self.q:
            if USE_POSTGRES:
                attendees = attendees.filter(
                    Q(first_name__unaccent__icontains=self.q)
                    | Q(last_name__unaccent__icontains=self.q)
                    | Q(nickname__unaccent__icontains=self.q)
                    | Q(email__icontains=self.q)
                )
            else:
                attendees = attendees.filter(
                    Q(first_name__icontains=self.q.lower())
                    | Q(last_name__icontains=self.q.lower())
                    | Q(nickname__icontains=self.q.lower())
                    | Q(email__icontains=self.q.lower())
                )
        return attendees[:5]


class AllAttendeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Attendee.objects.none()
        event_slug = self.forwarded.get("event_slug", None)
        event_user = EventUser.objects.filter(user=self.request.user, event__event_slug=event_slug).first()
        attendees = Attendee.objects.filter(event__event_slug=event_slug)
        if event_user and self.q:
            if USE_POSTGRES:
                attendees = attendees.filter(
                    Q(first_name__unaccent__icontains=self.q)
                    | Q(last_name__unaccent__icontains=self.q)
                    | Q(nickname__unaccent__icontains=self.q)
                    | Q(email__unaccent__icontains=self.q)
                )
            else:
                attendees = attendees.filter(
                    Q(first_name__icontains=self.q.lower())
                    | Q(last_name__icontains=self.q.lower())
                    | Q(nickname__icontains=self.q.lower())
                    | Q(email__icontains=self.q.lower())
                )
        return attendees[:5]


class EventUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return EventUser.objects.none()

        event_slug = self.forwarded.get("event_slug", None)
        event_user = EventUser.objects.filter(user=self.request.user, event__event_slug=event_slug).first()

        attended = [
            attendance_date.event_user.pk
            for attendance_date in EventUserAttendanceDate.objects.filter(
                event_user__event__event_slug=event_slug,
                date__date=datetime.date.today(),
            )
        ]

        event_users = EventUser.objects.filter(event=event_user.event).exclude(pk__in=attended)

        if event_user and self.q:
            if USE_POSTGRES:
                event_users = event_users.filter(
                    Q(user__first_name__unaccent__icontains=self.q)
                    | Q(user__last_name__unaccent__icontains=self.q)
                    | Q(user__username__unaccent__icontains=self.q)
                    | Q(user__email__unaccent__icontains=self.q)
                )
            else:
                event_users = event_users.filter(
                    Q(user__first_name__icontains=self.q.lower())
                    | Q(user__last_name__icontains=self.q.lower())
                    | Q(user__username__icontains=self.q.lower())
                    | Q(user__email__icontains=self.q.lower())
                )
        return event_users[:5]


class AttendeeSearchForm(forms.Form):
    def __init__(self, event_slug, *args, **kwargs):
        kwargs.update(
            initial={
                "event_slug": event_slug,
            }
        )

        super().__init__(*args, **kwargs)
        self.fields["event_slug"].widget = forms.HiddenInput()

    event_slug = forms.CharField()
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.all(),
        widget=autocomplete.ModelSelect2(url="attendee-autocomplete", forward=["event_slug"]),
        required=False,
        label=_("Attendee"),
    )


class EventUserSearchForm(forms.Form):
    def __init__(self, event_slug, *args, **kwargs):
        kwargs.update(
            initial={
                "event_slug": event_slug,
            }
        )
        super().__init__(*args, **kwargs)
        self.fields["event_slug"].widget = forms.HiddenInput()

    event_slug = forms.CharField()
    event_user = forms.ModelChoiceField(
        queryset=EventUser.objects.all(),
        widget=autocomplete.ModelSelect2(url="eventuser-autocomplete", forward=["event_slug"]),
        required=False,
        label=_("Collaborator/Installer"),
    )


class AttendeeRegistrationByCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = [
            "first_name",
            "last_name",
            "nickname",
            "email",
            "additional_info",
            "is_installing",
            "event",
            "registration_date",
        ]
        widgets = {
            "event": forms.HiddenInput(),
            "registration_date": forms.HiddenInput(),
            "additional_info": forms.TextInput(),
        }


class InstallationForm(forms.ModelForm):
    def __init__(self, event_slug, *args, **kwargs):
        kwargs.update(
            initial={
                "event_slug": event_slug,
            }
        )

        super().__init__(*args, **kwargs)
        self.fields["event_slug"].widget = forms.HiddenInput()

    event_slug = forms.CharField()

    class Meta:
        model = Installation
        fields = ("attendee", "notes", "software")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
            "attendee": autocomplete.ModelSelect2(url="all-attendee-autocomplete", forward=["event_slug"]),
            "software": autocomplete.ModelSelect2(url="software-autocomplete"),
        }


class HardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ("type", "manufacturer", "model")


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ["start_date", "end_date", "room", "event"]
        widgets = {
            "event": forms.HiddenInput(),
            "start_date": TimePicker(options={"format": "HH:mm"}),
            "end_date": TimePicker(options={"format": "HH:mm"}),
        }

    def __init__(self, event_slug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            choices = []
            event_dates = EventDate.objects.filter(event__event_slug=event_slug)
            for event_date in event_dates:
                date_value = date_format(event_date.date, format="SHORT_DATE_FORMAT", use_l10n=True)
                choices.append(
                    (
                        event_date.id,
                        date_value,
                    )
                )
            self.fields["room"].queryset = Room.objects.filter(event__event_slug=event_slug)
            self.fields["date"] = forms.ChoiceField(choices=choices)

            self.fields["start_date"].widget.attrs.update({"id": uuid.uuid4().hex.lower()})
            self.fields["end_date"].widget.attrs.update({"id": uuid.uuid4().hex.lower()})


class CollaboratorRegistrationForm(ModelForm):
    class Meta:
        model = Collaborator
        widgets = {"event_user": forms.HiddenInput()}
        fields = "__all__"


class AttendeeRegistrationFromUserForm(ModelForm):
    field_order = [
        "first_name",
        "last_name",
        "nickname",
        "additional_info",
        "is_installing",
        "email",
        "event",
        "event_user",
        "registration_date",
    ]

    class Meta:
        model = Attendee
        fields = [
            "first_name",
            "last_name",
            "nickname",
            "email",
            "additional_info",
            "is_installing",
            "event",
            "registration_date",
            "event_user",
        ]
        widgets = {
            "first_name": forms.HiddenInput(),
            "last_name": forms.HiddenInput(),
            "nickname": forms.HiddenInput(),
            "event": forms.HiddenInput(),
            "email": forms.HiddenInput(),
            "event_user": forms.HiddenInput(),
            "additional_info": forms.TextInput(),
            "registration_date": forms.HiddenInput(),
        }


class EventUserRegistrationForm(ModelForm):
    class Meta:
        model = EventUser
        fields = ["event"]
        widgets = {"event": forms.HiddenInput()}


class AttendeeRegistrationForm(ModelForm):
    repeat_email = forms.EmailField(label=_("Repeat Email"))
    captcha = CaptchaField()

    field_order = [
        "first_name",
        "last_name",
        "nickname",
        "additional_info",
        "is_installing",
        "email",
        "repeat_email",
        "captcha",
        "event",
        "registration_date",
    ]

    class Meta:
        model = Attendee
        fields = [
            "first_name",
            "last_name",
            "nickname",
            "email",
            "additional_info",
            "is_installing",
            "event",
            "registration_date",
        ]
        widgets = {
            "event": forms.HiddenInput(),
            "additional_info": forms.TextInput(),
            "registration_date": forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        repeat_email = cleaned_data.get("repeat_email")

        if email and email != repeat_email:
            raise forms.ValidationError(
                {
                    "email": _("Emails do not match."),
                    "repeat_email": _("Emails do not match."),
                }
            )

        return cleaned_data


class InstallerRegistrationForm(ModelForm):
    protocol = "https://"
    url = "wiki.antifa-glug.org/books/flisol-caba/page/guía-del-buen-instalador"
    target = "_blank"
    link_text = "Sagrada Guía del Buen Instalador"
    text = f'Afirmo que he leido la "<a href="{protocol}{url}" target="{target}">{link_text}</a>"'
    read_guidelines = forms.BooleanField(label=mark_safe(text), required=True)

    class Meta:
        model = Installer
        widgets = {"event_user": forms.HiddenInput()}
        fields = "__all__"


class ImageCroppingForm(ModelForm):
    class Meta:
        model = Activity
        fields = ("image", "cropping")
        widgets = {
            "image": ImageCropWidget,
        }


class EventImageCroppingForm(ModelForm):
    class Meta:
        model = Event
        fields = ("image", "cropping")
        widgets = {
            "image": ImageCropWidget,
        }


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["type", "url", "text"]

    def clean(self):
        cleaned_data = super().clean()
        data_type = cleaned_data.get("type")
        value = cleaned_data.get("url")

        if data_type:
            if data_type.validate == "1":
                try:
                    validator = URLValidator()
                    validator(value)
                except ValidationError:
                    self.add_error("url", "Enter valid URL")

            elif data_type.validate == "2":
                try:
                    validate_email(value)
                except ValidationError:
                    self.add_error("url", "Enter valid Email")
        else:  # data_type none
            self.add_error("type", _("This field is required"))
        return cleaned_data


class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = (
            "name",
            "email",
            "message",
        )
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class EventDateForm(ModelForm):
    class Meta:
        model = EventDate
        fields = ("date",)
        widgets = {"date": DatePicker()}


class EventDateModelFormset(BaseModelFormSet):
    @staticmethod
    def validate_date(date, dates):
        if date in dates:
            raise forms.ValidationError(
                _("One or more dates of the event are the same date"),
                code="duplicate_date",
            )

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        dates = []

        for form in self.forms:
            if form.cleaned_data:
                date = form.cleaned_data["date"]
                delete = form.cleaned_data[DELETION_FIELD_NAME]
                if date and not delete:
                    self.validate_date(date, dates)
                    dates.append(date)


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            "name",
            "event_slug",
            "limit_proposal_date",
            "registration_closed",
            "email",
            "place",
            "external_url",
            "abstract",
            "event_information",
            "use_installations",
            "use_installers",
            "is_flisol",
            "use_talks",
            "use_collaborators",
            "use_proposals",
            "use_schedule",
            "activities_proposal_form_text",
            "tags",
        )
        widgets = {"place": forms.HiddenInput(), "limit_proposal_date": DatePicker()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["limit_proposal_date"].required = False

    def clean(self):
        cleaned_data = super().clean()
        use_proposals = cleaned_data.get("use_proposals")
        limit_proposal_date = cleaned_data.get("limit_proposal_date")

        if use_proposals and not limit_proposal_date:
            self.add_error(
                "limit_proposal_date",
                "When the event uses proposals, this field is required",
            )
        elif not use_proposals:
            cleaned_data["limit_proposal_date"] = datetime.date.today()
        return cleaned_data


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = self.fields["login"].widget.attrs["placeholder"]
        self.fields["login"].label = label
        del self.fields["login"].widget.attrs["placeholder"]
        del self.fields["password"].widget.attrs["placeholder"]


class SignUpForm(AllAuthSignUpForm):
    first_name = forms.CharField(max_length=30, label=_("First Name"))
    last_name = forms.CharField(max_length=30, label=_("Last Name"))

    ordered_field_names = [
        "first_name",
        "last_name",
        "password1",
        "password2",
        "email",
        "email2",
        "username",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["username", "email", "email2", "password1", "password2"]:
            del self.fields[field].widget.attrs["placeholder"]

        original_fields = self.fields
        new_fields = OrderedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        for field in self.fields:
            if field not in self.ordered_field_names:
                new_fields[field] = original_fields.get(field)

        self.fields = new_fields

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


class ResetPasswordForm(AllAuthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["email"]:
            del self.fields[field].widget.attrs["placeholder"]


class ResetPasswordKeyForm(AllAuthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["password1", "password2"]:
            del self.fields[field].widget.attrs["placeholder"]


class ChangePasswordForm(AllAuthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["oldpassword", "password1", "password2"]:
            del self.fields[field].widget.attrs["placeholder"]


class SetPasswordForm(AllAuthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["password1", "password2"]:
            del self.fields[field].widget.attrs["placeholder"]


class SocialSignUpForm(AllAuthSocialSignUpForm):
    first_name = forms.CharField(max_length=30, label=_("First Name"))
    last_name = forms.CharField(max_length=30, label=_("Last Name"))

    ordered_field_names = ["email", "email2", "first_name", "last_name", "username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["username", "email", "email2"]:
            del self.fields[field].widget.attrs["placeholder"]

        original_fields = self.fields
        new_fields = OrderedDict()

        for field_name in self.ordered_field_names:
            field = original_fields.get(field_name)
            if field:
                new_fields[field_name] = field

        for field in self.fields:
            if field not in self.ordered_field_names:
                new_fields[field] = original_fields.get(field)

        self.fields = new_fields

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


class ActivityProposalForm(ModelForm):
    captcha = CaptchaField(label=_("Are you a human?"))

    field_order = [
        "event",
        "title",
        "speakers_names",
        "speaker_bio",
        "abstract",
        "long_description",
        "labels",
        "level",
        "activity_type",
        "presentation",
        "additional_info",
        "captcha",
        "status",
    ]

    class Meta:
        model = Activity
        fields = [
            "event",
            "title",
            "speakers_names",
            "speaker_bio",
            "abstract",
            "long_description",
            "labels",
            "presentation",
            "level",
            "additional_info",
            "status",
            "activity_type",
        ]
        widgets = {
            "event": forms.HiddenInput(),
            "status": forms.HiddenInput(),
            "speaker_bio": forms.Textarea(attrs={"rows": 3}),
            "abstract": forms.Textarea(attrs={"rows": 3}),
            "long_description": forms.Textarea(attrs={"rows": 3}),
            "additional_info": forms.Textarea(attrs={"rows": 3}),
        }


class ActivityDummyForm(ModelForm):
    field_order = ["event", "title", "abstract", "status"]

    class Meta:
        model = Activity
        fields = ["event", "title", "abstract", "status"]
        widgets = {
            "event": forms.HiddenInput(),
            "status": forms.HiddenInput(),
        }


class RejectForm(Form):
    justification = forms.CharField(required=False, label=_("Why do you reject this proposal?"))


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "event"]
        widgets = {"event": forms.HiddenInput()}
