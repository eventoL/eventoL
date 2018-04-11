import datetime
import re
from uuid import uuid4
from random import SystemRandom
from string import digits, ascii_lowercase, ascii_uppercase

from ckeditor.fields import RichTextField
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _, ugettext_noop as _noop
from image_cropping import ImageCropField, ImageRatioField


def validate_url(url):
    if not re.match('^[a-zA-Z0-9-_]+$', url):
        raise ValidationError(_('URL can only contain letters or numbers'))


def generate_ticket_code():
    chars = digits + ascii_lowercase + ascii_uppercase
    length = 21
    return ''.join([SystemRandom().choice(chars) for _ in range(length)])


class EventManager(models.Manager):
    def get_queryset(self):
        today = timezone.localdate()
        return super() \
            .get_queryset() \
            .annotate(attendees_count=models.Count('attendee')) \
            .annotate(last_date=models.Max('eventdate__date')) \
            .annotate(activity_proposal_is_open=models.Case(
                models.When(limit_proposal_date__gte=today, then=True),
                default=False,
                output_field=models.BooleanField()
            )) \
            .annotate(registration_is_open=models.Case(
                models.When(last_date__gte=today, then=True),
                default=False,
                output_field=models.BooleanField()
            ))


class Event(models.Model):
    objects = EventManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    name = models.CharField(_('Event Name'), max_length=50)
    abstract = models.TextField(_('Abstract'), max_length=250,
                                help_text=_('Short idea of the event (One or two sentences)'))
    limit_proposal_date = models.DateField(_('Limit Proposals Date'),
                                           help_text=_('Limit date to submit talk proposals'))
    slug = models.CharField(_('URL'), max_length=20,
                            help_text=_('For example: flisol-caba'),
                            validators=[validate_url])
    uid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        verbose_name=_('UID'),
        help_text=_('Unique identifier for the event'),
    )
    registration_code = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        verbose_name=_('code'),
        help_text=_('Code validator for in-place event self-registration'),
    )
    external_url = models.URLField(_('External URL'), blank=True, null=True, default=None,
                                   help_text=_('http://www.my-awesome-event.com'))
    email = models.EmailField(verbose_name=_('Email'))
    event_information = RichTextField(verbose_name=_('Event Information'),
                                      help_text=_('Event Information HTML'),
                                      blank=True, null=True)
    schedule_confirmed = models.BooleanField(_('Schedule Confirmed'), default=False)
    place = models.TextField(_('Place'))
    image = ImageCropField(upload_to='images_thumbnails',
                           verbose_name=_('Image'), blank=True, null=True)
    cropping = ImageRatioField('image', '700x450', size_warning=True,
                               verbose_name=_('Cropping'), free_crop=True,
                               help_text=_('The image must be 700x450 px. You can crop it here.'))

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        return '/event/{}/{}/'.format(self.slug, self.uid)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['name']


class EventDate(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              blank=True, null=True)
    date = models.DateField(_('Date'), help_text=_('When will your event be?'))

    def __str__(self):
        return '{} - {}'.format(self.event, self.date)


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    message = models.TextField(verbose_name=_('Message'))
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              blank=True, null=True)

    def __str__(self):
        return _(
            'Message received from: {name}\n'
            'User email: {email}\n\n'
            '{message}'
        ).format(
            name=self.name,
            email=self.email,
            message=self.message
        )

    class Meta(object):
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')


class ContactType(models.Model):
    """
    For example:
        Name: Facebook
        Icon Class: fa-facebook-square
    """
    validator_choices = (
        ('1', _('Validate URL')),
        ('2', _('Validate Email')),
        ('3', _('Don\'t validate'))
    )
    name = models.CharField(_('Name'), unique=True, max_length=200)
    icon_class = models.CharField(_('Icon Class'), max_length=200)
    validate = models.CharField(_('Level'), choices=validator_choices,
                                max_length=10,
                                help_text=_('Type of field validation'))

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contact Types')


class Contact(models.Model):
    type = models.ForeignKey(ContactType, verbose_name=_('Contact Type'))
    url = models.CharField(_noop('Direccion'),
                           help_text=_('i.e. https://twitter.com/flisol'),
                           max_length=200)
    text = models.CharField(_('Text'), max_length=200,
                            help_text=_('i.e. @Flisol'))
    # TODO: null should be false,
    # but I put true due to a django bug with formsets:
    # https://code.djangoproject.com/ticket/13776
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              related_name='contacts', blank=True, null=False)

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.type, self.text)

    class Meta(object):
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Ticket(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    sent = models.BooleanField(_('Sent'), default=False)
    code = models.CharField(
        max_length=21,
        default=generate_ticket_code,
        editable=False,
        unique=True,
        verbose_name=_('number'),
        help_text=_('Unique identifier for the ticket'),
    )

    def __str__(self):
        return self.code


class EventUser(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('User'),
                             blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'),
                               blank=True, null=True)

    def __str__(self):
        if self.user:
            return '{} - {} {}'.format(self.event, self.user.first_name, self.user.last_name)
        return '{}'.format(self.event)

    def get_ticket_data(self):
        if self.ticket is None:
            ticket = Ticket()
            ticket.save()
            self.ticket = ticket
            self.save()
        date = self.event.eventdate_set.order_by('date').first().date
        return {'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'nickname': self.user.username,
                'email': self.user.email, 'event': self.event,
                'event_date': date, 'ticket': self.ticket}

    def attended(self):
        return EventUserAttendanceDate.objects.filter(event_user=self).exists()

    def attended_today(self):
        return EventUserAttendanceDate.objects.filter(
            event_user=self, date__date=timezone.localdate()).exists()

    class Meta(object):
        unique_together = (('event', 'user'),)
        verbose_name = _('Event User')
        verbose_name_plural = _('Event Users')


class EventUserAttendanceDate(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_noop('Event User'),
                                   blank=False, null=False)
    date = models.DateTimeField(_('Date'),
                                help_text=_('The date of the attendance'),
                                auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.event_user, self.date)


class Collaborator(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True)
    assignation = models.CharField(_('Assignation'), max_length=200,
                                   blank=True, null=True,
                                   help_text=_('Anything you can help with (i.e. Talks, Coffee...)'))
    time_availability = models.CharField(_('Time Availability'),
                                         max_length=200, blank=True,
                                         null=True,
                                         help_text=_('Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon", ...'))
    phone = models.CharField(_('Phone'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200,
                               blank=True, null=True)
    additional_info = models.CharField(_('Additional Info'), max_length=200,
                                       blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant'))

    class Meta(object):
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')

    def __str__(self):
        return str(self.event_user)


class Organizer(models.Model):
    """Event organizer"""
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True)

    class Meta(object):
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')

    def __str__(self):
        return str(self.event_user)


class Attendee(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    first_name = models.CharField(_('First Name'), max_length=200, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=200, blank=True, null=True)
    nickname = models.CharField(_('Nickname'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('Email'))
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), blank=True, null=True)
    is_installing = models.BooleanField(_('Is going to install?'), default=False)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant for the organizers'))
    email_confirmed = models.BooleanField(_('Email confirmed?'), default=False)
    email_token = models.CharField(_('Confirmation Token'), max_length=200, blank=True, null=True)
    registration_date = models.DateTimeField(_('Registration Date'), blank=True, null=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_noop('Event User'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')
        unique_together = (('event', 'email'),)

    def __str__(self):
        if self.event_user:
            return str(self.event_user)
        return '{} - {} {} - {} - {}'.format(self.event, self.first_name, self.last_name,
                                             self.nickname, self.email)

    def get_ticket_data(self):
        if self.ticket is None:
            ticket = Ticket()
            ticket.save()
            self.ticket = ticket
            self.save()

        date = self.event.eventdate_set.order_by('date').first().date
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'nickname': self.nickname, 'email': self.email,
                'event': self.event, 'event_date': date, 'ticket': self.ticket}

    def attended(self):
        return AttendeeAttendanceDate.objects.filter(attendee=self).exists()

    def attended_today(self):
        return AttendeeAttendanceDate.objects.filter(
            attendee=self, date__date=timezone.localdate()).exists()


class AttendeeAttendanceDate(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    attendee = models.ForeignKey(Attendee, verbose_name=_noop('Attendee'),
                                 blank=False, null=False)
    date = models.DateTimeField(_('Date'),
                                help_text=_('The date of the attendance'),
                                auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.attendee, self.date)


class InstallationMessage(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'))
    message = RichTextField(verbose_name=_('Message Body'), help_text=_(
        'Email message HTML Body'), blank=True, null=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'))

    class Meta(object):
        verbose_name = _('Post-install Email')
        verbose_name_plural = _('Post-install Emails')

    def __str__(self):
        return str(self.event)


class Installer(models.Model):
    installer_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
        ('4', _('Super Hacker'))
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True)
    level = models.CharField(_('Level'), choices=installer_choices,
                             max_length=200,
                             help_text=_('Knowledge level for an installation'))

    class Meta(object):
        verbose_name = _('Installer')
        verbose_name_plural = _('Installers')

    def __str__(self):
        return str(self.event_user)


class Software(models.Model):
    software_choices = (
        ('OS', _('Operative System')),
        ('AP', _('Application')),
        ('SU', _('Support and Problem Fixing')),
        ('OT', _('Other'))
    )
    name = models.CharField(_('Name'), max_length=200)
    type = models.CharField(_('Type'),
                            choices=software_choices, max_length=200)

    def __str__(self):
        return '{} - {}'.format(self.type, self.name)


class Hardware(models.Model):
    hardware_choices = (
        ('MOB', _('Mobile')),
        ('NOTE', _('Notebook')),
        ('NET', _('Netbook')),
        ('TAB', _('Tablet')),
        ('DES', _('Desktop')),
        ('OTH', _('Other'))
    )
    type = models.CharField(_('Type'), choices=hardware_choices,
                            max_length=200)
    manufacturer = models.CharField(_('Manufacturer'), max_length=200,
                                    blank=True, null=True)
    model = models.CharField(_('Model'), max_length=200, blank=True, null=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.type, self.manufacturer, self.model)


class Room(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              blank=True, null=True)
    name = models.CharField(_('Name'), max_length=200,
                            help_text=_('i.e. Classroom 256'))

    def __str__(self):
        return '{} - {}'.format(self.event, self.name)

    def get_schedule_info(self):
        return {'id': self.pk, 'title': self.name}

    class Meta(object):
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['name']


class Activity(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    title = models.CharField(_('Title'), max_length=50,
                             blank=False, null=False)
    long_description = models.TextField(_('Long Description'))
    abstract = models.TextField(_('Abstract'),
                                help_text=_('Short idea of the talk (Two or three sentences)'))
    room = models.ForeignKey(Room, verbose_name=_('Room'),
                             blank=True, null=True)
    start_date = models.DateTimeField(_('Start Time'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Time'), blank=True, null=True)
    activity_type_choices = (
        ('1', _('Talk')),
        ('2', _('Workshop')),
        ('3', _('Lightning talk'))
    )
    type = models.CharField(_('Type'), choices=activity_type_choices, max_length=200, null=True, blank=True)
    speakers_names = models.CharField(_('Speakers Names'), max_length=600,
                                      help_text=_("Comma separated speaker's names"))
    speaker_contact = models.EmailField(_('Speaker Contact'),
                                        help_text=_('Where can whe reach you from the organization team?'))
    labels = models.CharField(_('Labels'), max_length=200,
                              help_text=_('Comma separated tags. i.e. Linux, Free Software, Archlinux'))
    presentation = models.FileField(_('Presentation'),
                                    upload_to='talks', blank=True,
                                    null=True, help_text=_('Any material you are going to use for the talk (optional, but recommended)'))
    level_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
    )
    level = models.CharField(_('Level'), choices=level_choices, max_length=100,
                             help_text=_("Talk's Technical level"))
    additional_info = models.TextField(_('Additional Info'),
                                       blank=True, null=True,
                                       help_text=_('Any info you consider relevant for the organizer: i.e. Write here if your activity has any special requirement'))

    status_choices = (
        ('1', _('Proposal')),
        ('2', _('Accepted')),
        ('3', _('Rejected')),
    )

    status = models.CharField(_('Status'), choices=status_choices, max_length=20,
                              help_text=_('Activity proposal status'))

    image = ImageCropField(upload_to='images_thumbnails',
                           verbose_name=_('Image'), blank=True, null=True)
    cropping = ImageRatioField('image', '700x450', size_warning=True,
                               verbose_name=_('Cropping'),
                               help_text=_('The image must be 700x450 px. You can crop it here.'))

    is_dummy = models.BooleanField(_('Is a dummy Activity?'), default=False,
                                   help_text=_('A dummy activity is used for example for coffee breaks. We use this to exclude it from the index page and other places'))

    def __cmp__(self, other):
        return -1 if self.start_date.time() < other.start_date.time() else 1

    def __str__(self):
        return '{} - {}'.format(self.event, self.title)

    def get_absolute_url(self):
        return reverse('activity_detail', args=(self.event.slug, self.event.uid, self.pk))

    def get_schedule_info(self):
        schedule_info = {
            'resourceId': self.room.pk,
            'start': self.start_date.isoformat(),
            'end': self.end_date.isoformat(),
            'title': self.title,
            'id': self.pk,
            'url': ""
        }

        if not self.is_dummy:
            schedule_info['url'] = self.get_absolute_url()

        return schedule_info

    def schedule(self):
        if self.start_date and self.end_date:
            date = date_format(self.start_date, format='SHORT_DATE_FORMAT', use_l10n=True)
            return "{} - {} - {}".format(self.start_date.strftime("%H:%M"), self.end_date.strftime("%H:%M"), date)
        return _('Schedule not confirmed yet')

    @classmethod
    def check_status(cls, message, error=None, request=None):
        if error:
            raise ValidationError(message)
        if request:
            messages.error(request, message)

    @classmethod
    def room_available(cls, request, proposal, event_uid, event_date, error=False):
        activities_room = Activity.objects.filter(room=proposal.room, event__uid=event_uid, start_date__date=event_date)
        if proposal.start_date == proposal.end_date:
            message = _("The talk couldn't be registered because the schedule not available (start time equals end time)")
            cls.check_status(message, error=error, request=request)
            return False
        if proposal.end_date < proposal.start_date:
            message = _("The talk couldn't be registered because the schedule is not available (start time is after end time)")
            cls.check_status(message, error=error, request=request)
            return False
        one_second = datetime.timedelta(seconds=1)
        if activities_room.filter(
                end_date__range=(proposal.start_date + one_second, proposal.end_date - one_second)).exclude(pk=proposal.pk).exists() \
                or activities_room.filter(end_date__gt=proposal.end_date, start_date__lt=proposal.start_date).exclude(pk=proposal.pk).exists() \
                or activities_room.filter(start_date__range=(proposal.start_date + one_second, proposal.end_date - one_second)).exclude(pk=proposal.pk).exists() \
                or activities_room.filter(
                    end_date=proposal.end_date, start_date=proposal.start_date).exclude(pk=proposal.pk).exists():
                message = _("The talk couldn't be registered because the room or the schedule is not available")
                cls.check_status(message, error=error, request=request)
                return False
        return True

    class Meta(object):
        ordering = ['title']
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class Installation(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    hardware = models.ForeignKey(Hardware, verbose_name=_('Hardware'),
                                 blank=True, null=True)
    software = models.ForeignKey(Software, verbose_name=_('Software'),
                                 blank=True, null=True)
    attendee = models.ForeignKey(Attendee, verbose_name=_('Attendee'),
                                 help_text=_('The owner of the installed hardware'))
    installer = models.ForeignKey(EventUser, verbose_name=_('Installer'),
                                  related_name='installed_by', blank=True,
                                  null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True,
                             help_text=_('Any information or trouble you found and consider relevant to document'))

    def __str__(self):
        return '{}, {}, {}'.format(self.attendee, self.hardware, self.software)

    class Meta(object):
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')
