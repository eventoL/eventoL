# pylint: disable=arguments-differ
# pylint: disable=too-many-lines

import datetime
import itertools
import json
import logging
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
from django.utils.translation import gettext as _, gettext_noop as _noop
from image_cropping import ImageCropField, ImageRatioField
from django_jsonfield_backport.models import JSONField

from vote.models import VoteModel
from manager.utils.report import count_by
from manager.utils.slug import get_unique_slug

logger = logging.getLogger('eventol')


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
            .annotate(attendees_count=models.Count('attendee', distinct=True)) \
            .annotate(last_date=models.Max('eventdate__date')) \
            .annotate(activity_proposal_is_open=models.Case(
                models.When(models.Q(limit_proposal_date__gte=today), then=True),
                default=False,
                output_field=models.BooleanField()
            )) \
            .annotate(registration_is_open=models.Case(
                models.When(models.Q(last_date__gte=today), then=True),
                default=False,
                output_field=models.BooleanField()
            ))

    @staticmethod
    def get_event_by_user(user, tag_slug=None):
        if user.is_authenticated:
            event_users = EventUser.objects.filter(user=user)
            event_ids = [event_user.event.pk for event_user in list(event_users)]
            queryset = Event.objects.filter(pk__in=event_ids)
            if tag_slug:
                queryset = queryset.filter(tags__slug=tag_slug)
        else:
            queryset = Event.objects.none()
        return queryset

    @staticmethod
    def get_event_private_data():
        events = []
        for event in Event.objects.all():
            organizers = Organizer.objects.filter(event_user__event=event)
            users = map(lambda organizer: organizer.event_user.user, organizers)
            full_names = [user.get_full_name() for user in users]
            events.append({
                'organizers': ','.join(full_names),
                'email': event.email,
                'id': event.id
            })
        return events


class EventTag(models.Model):
    """A Event grouper"""
    name = models.CharField(_('EventTag Name'), max_length=50, unique=True,
                            help_text=_("This name will be used as a slug"))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    background = models.ImageField(
        null=True, blank=True,
        help_text=_("A image to show in the background of"))
    logo_header = models.ImageField(
        null=True, blank=True,
        help_text=_("This logo will be shown in the right corner of the page"))
    logo_landing = models.ImageField(
        null=True, blank=True,
        help_text=_("Logo to show in the center of the page"))
    message = models.TextField(max_length=280, null=True, blank=True,
                               help_text=_("A message to show in the center of the page"))
    slug = models.SlugField(_('URL'), max_length=100,
                            help_text=_('For example: flisol-caba'), unique=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override default save

        it will add the slug field using slugify.
        """
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

class Event(models.Model):
    objects = EventManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    name = models.CharField(_('Event Name'), max_length=50)
    abstract = models.TextField(_('Abstract'), max_length=250,
                                help_text=_('Idea of the event \
                                            (one or two sentences)'))
    limit_proposal_date = models.DateField(_('Limit Proposals Date'),
                                           help_text=_('Limit date to submit talk proposals'))
    registration_closed = models.BooleanField(
        default=False, help_text=_("set it to True to force the registration to be closed"))

    tags = models.ManyToManyField(
        EventTag, blank=True, help_text=_("Select tags to show this event in the EventTag landing"))
    event_slug = models.SlugField(_('URL'), max_length=100,
                                  help_text=_('For example: flisol-caba'), unique=True)
    cname = models.CharField(_('CNAME'), max_length=50, blank=True, null=True,
                             help_text=_('For example: flisol-caba'),
                             validators=[validate_url])
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
    event_information = RichTextField(verbose_name=_('Event Info'),
                                      help_text=_('Event Info HTML'),
                                      blank=True, null=True)
    schedule_confirmed = models.BooleanField(_('Schedule Confirmed'), default=False)
    use_installations = models.BooleanField(_('Use Installations'), default=True)
    use_installers = models.BooleanField(_('Use Installers'), default=True)
    use_collaborators = models.BooleanField(_('Use Collaborators'), default=True)
    use_proposals = models.BooleanField(_('Use Proposals'), default=True)
    use_talks = models.BooleanField(_('Use Talks'), default=True)
    is_flisol = models.BooleanField(_('Is FLISoL'), default=False)
    use_schedule = models.BooleanField(_('Use Schedule'), default=True)
    place = models.TextField(_('Place'), null=True, blank=True)
    image = ImageCropField(upload_to='images_thumbnails',
                           verbose_name=_('Image'), blank=True, null=True)
    cropping = ImageRatioField('image', '700x450', size_warning=True,
                               verbose_name=_('Cropping'), free_crop=True,
                               help_text=_('The image must be 700x450 px. You can crop it here.'))
    activities_proposal_form_text = RichTextField(
        verbose_name=_('Activity proposal form text'),
        help_text=_("A message to show in the activities proposal form"),
        blank=True, null=True
    )
    template = models.FileField(_('Template'),
                                upload_to='templates', blank=True, null=True,
                                help_text=_('Custom template HTML for event index page'))
    css_custom = models.FileField(_('Custom CSS'),
                                  upload_to='custom_css', blank=True, null=True,
                                  help_text=_('Custom CSS file for event page'))

    @classmethod
    def get_fields_dependencies(cls):
        return {
            'use_proposals': ['limit_proposal_date', 'activities_proposal_form_text'],
            'use_talks': ['use_proposals'],
            'use_installations': ['use_installers']
        }

    @property
    def location(self):
        try:
            place = json.loads(self.place)
            components = place['address_components']
            components = filter(
                lambda componet: 'political' in componet['types'],
                components
            )
            components = map(
                lambda componet: componet['long_name'],
                components
            )
            return components
        except json.JSONDecodeError as error:
            logger.error(error)
        except:
            pass
        return []

    @property
    def report(self):
        event_user = EventUser.objects.get_counts_by_event(self)
        collaborator = Collaborator.objects.get_counts_by_event(self)
        organizer = Organizer.objects.get_counts_by_event(self)
        attendee = Attendee.objects.get_counts_by_event(self)
        installer = Installer.objects.get_counts_by_event(self)
        activity = Activity.objects.get_counts_by_event(self)
        installation = Installation.objects.get_counts_by_event(self)
        speakers = []
        for talk in Activity.objects.filter(event=self, status='2'):
            speakers.append(talk.speakers_names.split(','))
        speakers_count = len(set(itertools.chain.from_iterable(speakers)))
        return {
            'event_user': event_user,
            'collaborator': collaborator,
            'organizer': organizer,
            'attendee': attendee,
            'installer': installer,
            'activity': activity,
            'installation': installation,
            'speakers': speakers_count
        }

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        return reverse('index', kwargs={'event_slug': self.event_slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def save(self, *args, **kwargs):
        """
        Override default save

        it will add the slug field using slugify.
        """
        if not self.event_slug:
            self.event_slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class EventDate(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(_('Date'), help_text=_('When will your event be?'))

    def __str__(self):
        return '{} - {}'.format(self.event, self.date)

    class Meta:
        verbose_name = _('Event Date')
        verbose_name_plural = _('Event Dates')


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    message = models.TextField(verbose_name=_('Message'))
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return _noop(
            'Message received from: {name}\n'
            'User email: {email}\n\n'
            '{message}'
        ).format(
            name=self.name,
            email=self.email,
            message=self.message
        )

    class Meta:
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

    class Meta:
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contact Types')


class Contact(models.Model):
    type = models.ForeignKey(ContactType, verbose_name=_('Contact Type'),on_delete=models.CASCADE)
    url = models.CharField(_noop('Direccion'),
                           help_text=_('i.e. https://twitter.com/flisol'),
                           max_length=200)
    text = models.CharField(_('Text'), max_length=200,
                            help_text=_('i.e. @Flisol'))
    event = models.ForeignKey(Event, verbose_name=_noop('Event'),
                              related_name='contacts', blank=True, null=False,on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.type, self.text)

    class Meta:
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


class EventUserManager(models.Manager):
    @staticmethod
    def get_event_user(instance):
        if hasattr(instance, 'event_user'):
            return instance.event_user
        return instance

    @staticmethod
    def get_counts(event_users):
        confirmed = EventUserAttendanceDate.objects \
            .filter(event_user__in=event_users) \
            .order_by('event_user') \
            .distinct() \
            .count()
        total = len(event_users)
        return {
            'total': total,
            'confirmed': confirmed,
            'not_confirmed': total - confirmed
        }

    def get_counts_by_event(self, event):
        model = self.model
        if hasattr(model, 'event_user'):
            queryset = model.objects.filter(event_user__event=event)
        else:
            queryset = model.objects.filter(event=event)
        event_users = self.get_event_users(queryset)
        return self.get_counts(event_users)

    def get_event_users(self, queryset):
        return [self.get_event_user(instance) for instance in queryset]


class EventUser(models.Model):
    objects = EventUserManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('User'),
                             blank=True, null=True,on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name=_('Event'),on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'),
                               blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        if self.user:
            return '{} at event:{}'.format(self.user.username, self.event)
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

    class Meta:
        unique_together = (('event', 'user'),)
        verbose_name = _('Event User')
        verbose_name_plural = _('Event Users')


class EventUserAttendanceDate(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_noop('Event User'),
                                   blank=False, null=False,on_delete=models.CASCADE)
    date = models.DateTimeField(_('Date'),
                                help_text=_('The date of the attendance'),
                                auto_now_add=True)
    attendance_mode_choices = (
        ('1', _('Qr autoregistration')),
        ('2', _('Qr ticket')),
        ('3', _('Previous registration')),
        ('4', _('unregistred'))
    )
    mode = models.CharField(_('Mode'), choices=attendance_mode_choices,
                            max_length=200, blank=True, null=True,
                            help_text=_('Attendance mode'))

    def __str__(self):
        return '{} - {}'.format(self.event_user, self.date)


class Collaborator(models.Model):
    objects = EventUserManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True, on_delete=models.CASCADE)
    assignation = models.CharField(_('Assignation'), max_length=200,
                                   blank=True, null=True,
                                   help_text=_('Anything you can help with \
                                               (i.e. Talks, Coffee…)'))
    time_availability = models.CharField(_('Time Availability'),
                                         max_length=200, blank=True,
                                         null=True,
                                         help_text=_('Time period in which you can \
                                                     help during the event. i.e. \
                                                     "All the event", "Morning", \
                                                     "Afternoon", …'))
    phone = models.CharField(_('Phone'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200,
                               blank=True, null=True)
    additional_info = models.CharField(_('Additional Info'), max_length=200,
                                       blank=True, null=True,
                                       help_text=_('Additional info you consider relevant'))

    class Meta:
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')

    def __str__(self):
        return str(self.event_user)


class Organizer(models.Model):
    """Event organizer"""
    objects = EventUserManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')

    def __str__(self):
        return str(self.event_user)


class Reviewer(models.Model):
    """User that collaborates with activities review"""
    objects = EventUserManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event_user)


class AttendeeManager(EventUserManager):
    @staticmethod
    def get_attendees(queryset):
        return [inst for inst in queryset if not inst.event_user]

    #pylint: disable=arguments-differ
    def get_counts(self, queryset):
        event_users = self.get_event_users(
            queryset.filter(event_user__isnull=False))
        confirmed_with_event_user = AttendeeAttendanceDate.objects \
            .filter(attendee__event_user__in=event_users) \
            .order_by('attendee__event_user') \
            .distinct() \
            .count()
        total_with_event_user = len(event_users)
        attendees = self.get_attendee(queryset)
        confirmed = AttendeeAttendanceDate.objects \
            .filter(
                attendee__in=attendees, attendee__event_user__isnull=True) \
            .order_by('attendees') \
            .distinct() \
            .count()
        total = len(attendees)
        return {
            'with_event_user': {
                'total': total_with_event_user,
                'confirmed': confirmed_with_event_user,
                'not_confirmed':
                    total_with_event_user - confirmed_with_event_user
            },
            'without_event_user': {
                'total': total,
                'confirmed': confirmed,
                'not_confirmed': total - confirmed
            }
        }

    def get_counts_by_event(self, event):
        queryset = Attendee.objects.filter(event=event)
        return self.get_counts(queryset)


class Attendee(models.Model):
    objects = AttendeeManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    first_name = models.CharField(_('First Name'), max_length=200, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=200, blank=True, null=True)
    nickname = models.CharField(_('Nickname'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('Email'))
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), blank=True, null=True, on_delete=models.CASCADE)
    is_installing = models.BooleanField(_('Is going to install?'), default=False)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Additional info you consider \
                                                   relevant to the organizers'))
    email_confirmed = models.BooleanField(_('Email confirmed?'), default=False)
    email_token = models.CharField(_('Confirmation Token'), max_length=200, blank=True, null=True)
    registration_date = models.DateTimeField(_('Registration Date'), blank=True, null=True)
    event_user = models.ForeignKey(
        EventUser, verbose_name=_noop('Event User'), blank=True, null=True, on_delete=models.CASCADE)
    customFields = JSONField(default=dict)

    class Meta:
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
                                 blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(_('Date'),
                                help_text=_('The date of the attendance'),
                                auto_now_add=True)
    attendance_mode_choices = (
        ('1', _('Qr autoregistration')),
        ('2', _('Qr ticket')),
        ('3', _('Previous registration')),
        ('4', _('unregistred'))
    )
    mode = models.CharField(_('Mode'), choices=attendance_mode_choices,
                            max_length=200, blank=True, null=True,
                            help_text=_('Attendance mode'))

    def __str__(self):
        return '{} - {}'.format(self.attendee, self.date)


class InstallationMessage(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), on_delete=models.CASCADE)
    message = RichTextField(verbose_name=_('Message Body'), help_text=_(
        'Email message HTML Body'), blank=True, null=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'))

    class Meta:
        verbose_name = _('Post-install Email')
        verbose_name_plural = _('Post-install Emails')

    def __str__(self):
        return str(self.event)


class Installer(models.Model):
    objects = EventUserManager()
    installer_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
        ('4', _('Super Hacker'))
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'),
                                   blank=True, null=True, on_delete=models.CASCADE)
    level = models.CharField(_('Level'), choices=installer_choices,
                             max_length=200,
                             help_text=_('Knowledge level for an installation'))

    class Meta:
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
                              blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=200,
                            help_text=_('i.e. Classroom 256'))

    def __str__(self):
        return '{} - {}'.format(self.event, self.name)

    def get_schedule_info(self):
        return {'id': self.pk, 'title': self.name}

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['name']


class ActivityManager(models.Manager):
    @staticmethod
    def get_counts(queryset):
        level_count = count_by(queryset, lambda activity: activity.level)
        status_count = count_by(queryset, lambda activity: activity.status)
        type_count = count_by(queryset, lambda activity: activity.activity_type)
        total = queryset.count()
        confirmed = queryset.filter(room__isnull=False).count()
        return {
            'level_count': level_count,
            'status_count': status_count,
            'type_count': type_count,
            'confirmed': confirmed,
            'not_confirmed': total - confirmed,
            'total': total
        }

    @staticmethod
    def get_activities_report(event):
        activities = Activity.objects.filter(event=event, is_dummy=False)
        return activities.values(
            'id', 'title', 'abstract', 'long_description',
            'activity_type', 'labels', 'level', 'additional_info',
            'speakers_names', 'owner__user__username', 'owner__user__first_name',
            'owner__user__last_name', 'owner__user__email', 'speaker_bio'
        )

    def get_counts_by_event(self, event):
        queryset = Activity.objects.filter(event=event)
        return self.get_counts(queryset)


class ActivityType(models.Model):
    """User created type of activities"""
    name = models.CharField(max_length=60, help_text=_("Kind of activity"))

    def __str__(self):
        return self.name


class Activity(VoteModel, models.Model):
    objects = ActivityManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.CASCADE)
    owner = models.ForeignKey(
        EventUser, help_text=_("Speaker or the person in charge of the activity"), on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=100,
                             blank=False, null=False)
    long_description = models.TextField(_('Long Description'))
    abstract = models.TextField(_('Abstract'),
                                help_text=_('Short idea of the talk (Two or three sentences)'))
    justification = models.TextField(_('Justification'), blank=True, null=True,
                                     help_text=_('Why do you reject this proposal?'))
    room = models.ForeignKey(Room, verbose_name=_('Room'),
                             blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(_('Start Time'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Time'), blank=True, null=True)
    activity_type = models.ForeignKey(ActivityType, verbose_name=_('Activity Type'), on_delete=models.CASCADE)
    speakers_names = models.CharField(_('Speakers Names'), max_length=600,
                                      help_text=_("Comma separated speaker names"))
    speaker_bio = models.TextField(
        _('Speaker Bio'), null=True,
        help_text=_('Tell us about you (we will use it as your "bio" in our website)'))
    labels = models.CharField(_('Labels'), max_length=200,
                              help_text=_('Comma separated tags. i.e. Linux, \
                                          Free Software, Devuan'))
    presentation = models.FileField(_('Presentation'),
                                    upload_to='talks', blank=True, null=True,
                                    help_text=_('Material you are going to use \
                                                for the talk (optional, but recommended)'))
    level_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
    )
    level = models.CharField(_('Level'), choices=level_choices, max_length=100,
                             help_text=_("Talk's Technical level"))
    additional_info = models.TextField(_('Additional Info'),
                                       blank=True, null=True,
                                       help_text=_('Info you consider relevant \
                                                   to the organizer, special \
                                                   activity requirements, etc.'))

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
                               verbose_name=_('Cropping'), free_crop=True,
                               help_text=_('The image must be 700x450 px. You can crop it here.'))

    is_dummy = models.BooleanField(_('Is a dummy Activity?'), default=False,
                                   help_text=_('A dummy activity is used for example for coffee \
                                               breaks. We use this to exclude it from the index \
                                               page and other places'))

    def __cmp__(self, other):
        return -1 if self.start_date.time() < other.start_date.time() else 1

    def __str__(self):
        return '{} - {}'.format(self.event, self.title)

    def get_absolute_url(self):
        return reverse('activity_detail', args=(self.event.event_slug, self.pk))

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
            return "{} - {} - {}".format(
                self.start_date.strftime("%H:%M"), self.end_date.strftime("%H:%M"), date)
        return _('Schedule not confirmed yet')

    @classmethod
    def check_status(cls, message, error=None, request=None):
        if error:
            raise ValidationError(message)
        if request:
            messages.error(request, message)

    # pylint: disable=too-many-arguments
    @classmethod
    def room_available(cls, request, proposal,
                       event_slug, event_date,
                       error=False):
        activities_room = Activity.objects.filter(
            room=proposal.room, event__event_slug=event_slug, start_date__date=event_date)
        if proposal.start_date == proposal.end_date:
            message = _("The talk couldn't be registered because the schedule is not \
                        available (starts and ends at the same time)")
            cls.check_status(message, error=error, request=request)
            return False
        if proposal.end_date < proposal.start_date:
            message = _("The talk couldn't be registered because the schedule is not \
                        available (starts after it finishes)")
            cls.check_status(message, error=error, request=request)
            return False
        one_second = datetime.timedelta(seconds=1)
        if activities_room.filter(
                end_date__range=(
                    proposal.start_date + one_second, proposal.end_date - one_second)) \
                .exclude(pk=proposal.pk).exists() \
                or activities_room.filter(
                    end_date__gt=proposal.end_date,
                    start_date__lt=proposal.start_date).exclude(pk=proposal.pk).exists() \
                or activities_room.filter(
                    start_date__range=(
                        proposal.start_date + one_second, proposal.end_date - one_second)) \
                    .exclude(pk=proposal.pk).exists() \
                or activities_room.filter(
                    end_date=proposal.end_date,
                    start_date=proposal.start_date).exclude(pk=proposal.pk).exists():
            message = _("The talk couldn't be registered because the \
                            room or the schedule is not available")
            cls.check_status(message, error=error, request=request)
            return False
        return True

    class Meta:
        ordering = ['title']
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class InstallationManager(models.Manager):
    @staticmethod
    def get_counts(queryset):
        hardware_count = count_by(
            queryset, lambda activity: activity.hardware.model)
        software_count = count_by(
            queryset, lambda activity: activity.software.name)
        installer_count = count_by(
            queryset, lambda activity: activity.installer.id)
        total = queryset.count()
        return {
            'hardware_count': hardware_count,
            'software_count': software_count,
            'installer_count': installer_count,
            'total': total
        }

    def get_counts_by_event(self, event):
        queryset = Installation.objects.filter(installer__event=event)
        return self.get_counts(queryset)


class Installation(models.Model):
    objects = InstallationManager()
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    hardware = models.ForeignKey(Hardware, verbose_name=_('Hardware'),
                                 blank=True, null=True, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, verbose_name=_('Software'),
                                 blank=True, null=True, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, verbose_name=_('Attendee'),
                                 help_text=_('The owner of the installed hardware'), on_delete=models.CASCADE)
    installer = models.ForeignKey(EventUser, verbose_name=_('Installer'),
                                  related_name='installed_by', blank=True,
                                  null=True, on_delete=models.CASCADE)
    notes = models.TextField(_('Notes'), blank=True, null=True,
                             help_text=_('Info or trouble you \
                                         consider relevant to document'))

    def __str__(self):
        return '{}, {}, {}'.format(self.attendee, self.hardware, self.software)

    class Meta:
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')


class EventolSetting(models.Model):
    background = models.ImageField(
        null=True, blank=True,
        help_text=_("A image to show in the background of"))
    logo_header = models.ImageField(
        null=True, blank=True,
        help_text=_("This logo will be shown in the right corner of the page"))
    logo_landing = models.ImageField(
        null=True, blank=True,
        help_text=_("Logo to show in the center of the page"))
    message = models.TextField(max_length=280, null=True, blank=True,
                               help_text=_("A message to show in the center of the page"))

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'eventoL configuration'

    def save(self, *args, **kwargs):
        self.pk = 1
        super(EventolSetting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        verbose_name = _('eventoL setting')
        verbose_name_plural = _('eventoL settings')
