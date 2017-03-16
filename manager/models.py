import datetime
import re

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext_noop as _noop
from image_cropping import ImageCropField, ImageRatioField


def validate_url(url):
    if not re.match("^[a-zA-Z0-9-_]+$", url):
        raise ValidationError(_('URL can only contain letters or numbers'))


class Event(models.Model):
    name = models.CharField(_('Event Name'), max_length=200)
    date = models.DateField(_('Date'), help_text=_('When will your event be?'))
    limit_proposal_date = models.DateField(_('Limit Proposals Date'),
                                           help_text=_('Limit date to submit talk proposals'))
    slug = models.CharField(_('URL'), max_length=200, unique=True, help_text=_('For example: flisol-caba'),
                            validators=[validate_url])
    external_url = models.URLField(_('External URL'), blank=True, null=True, default=None,
                                   help_text=_('http://www.my-awesome-event.com'))
    email = models.EmailField(verbose_name=_('Email'))
    event_information = RichTextField(verbose_name=_('Event Information'), help_text=_('Event Information HTML'),
                                      blank=True, null=True)
    schedule_confirmed = models.BooleanField(_('Schedule Confirmed'), default=False)
    place = models.TextField(_('Place'))  # TODO: JsonFIELD

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        return "/event/" + self.slug + '/'

    @property
    def activity_proposal_is_open(self):
        return self.limit_proposal_date >= datetime.date.today()

    @property
    def registration_is_open(self):
        return self.date >= datetime.date.today()

    def __unicode__(self):
        return u"%s" % self.name

    class Meta(object):
        ordering = ['name']


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    message = models.TextField(verbose_name=_('Message'))
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), blank=True, null=True)

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
    validate = models.CharField(_('Level'), choices=validator_choices, max_length=10,
                                help_text=_('Type of field validation'))

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contact Types')


class Contact(models.Model):
    type = models.ForeignKey(ContactType, verbose_name=_('Contact Type'))
    url = models.CharField(_noop('Direccion'), help_text=_('i.e. https://twitter.com/flisol'), max_length=200)
    text = models.CharField(_('Text'), max_length=200, help_text=_('i.e. @Flisol'))
    # TODO: null should be false, but I put true due to a django bug with formsets:
    # https://code.djangoproject.com/ticket/13776
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), related_name='contacts', blank=True, null=False)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.event.name, self.type.name, self.text)

    class Meta(object):
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Ticket(models.Model):
    sent = models.BooleanField(_('Sent'), default=False)

    def __unicode__(self):
        return u"%d" % self.id


class EventUser(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    attended = models.BooleanField(_('Attended'), default=False)
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), blank=True, null=True)

    def __unicode__(self):
        if self.user:
            return u'%s %s' % (self.user.first_name, self.user.last_name)

    def get_ticket_data(self):
        if self.ticket is None:
            ticket = Ticket()
            ticket.save()
            self.ticket = ticket
            self.save()
        return {'first_name': self.user.first_name, 'last_name': self.user.last_name, 'nickname': self.user.username,
                'email': self.user.email, 'event': self.event, 'ticket': self.ticket}

    class Meta(object):
        unique_together = (("event", "user"),)
        verbose_name = _('Event User')
        verbose_name_plural = _('Event Users')


class Collaborator(models.Model):
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'), blank=True, null=True)
    assignation = models.CharField(_('Assignation'), max_length=200, blank=True, null=True,
                                   help_text=_('Anything you can help with (i.e. Talks, Coffee...)'))
    time_availability = models.CharField(_('Time Availability'), max_length=200, blank=True, null=True, help_text=_(
        'Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon", ...'))
    phone = models.CharField(_('Phone'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200, blank=True, null=True)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant'))

    class Meta(object):
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')

    def __unicode__(self):
        return u'%s %s' % (self.event_user.user.first_name, self.event_user.user.last_name)


class Organizer(models.Model):
    """Event organizer"""
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')

    def __unicode__(self):
        return u'%s %s' % (self.event_user.user.first_name, self.event_user.user.last_name)


class Attendee(models.Model):
    first_name = models.CharField(_('First Name'), max_length=200, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=200, blank=True, null=True)
    nickname = models.CharField(_('Nickname'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('Email'))
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    attended = models.BooleanField(_('Attended'), default=False)
    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), blank=True, null=True)
    is_installing = models.BooleanField(_('Is going to install?'), default=False)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant for the organizers'))
    email_confirmed = models.BooleanField(_('Email confirmed?'), default=False)
    email_token = models.CharField(_('Confirmation Token'), max_length=200, blank=True, null=True)
    registration_date = models.DateTimeField(_('Registration Date'), blank=True, null=True)
    attendance_date = models.DateTimeField(_('Attendance Date'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')
        unique_together = (("event", "email"),)

    def __unicode__(self):
        return u'%s %s - %s - %s' % (self.first_name, self.last_name, self.nickname, self.email)

    def get_ticket_data(self):
        if self.ticket is None:
            ticket = Ticket()
            ticket.save()
            self.ticket = ticket
            self.save()
        return {'first_name': self.first_name, 'last_name': self.last_name, 'nickname': self.nickname,
                'email': self.email, 'event': self.event, 'ticket': self.ticket}


class InstallationMessage(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'))
    message = RichTextField(verbose_name=_('Message Body'), help_text=_(
        'Email message HTML Body'), blank=True, null=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'))

    class Meta(object):
        verbose_name = _('Post-install Email')
        verbose_name_plural = _('Post-install Emails')

    def __unicode__(self):
        return "%s post-install message" % self.event.name


class Installer(models.Model):
    installer_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
        ('4', _('Super Hacker'))
    )
    event_user = models.ForeignKey(EventUser, verbose_name=_('Event User'), blank=True, null=True)
    level = models.CharField(_('Level'), choices=installer_choices, max_length=200,
                             help_text=_('Knowledge level for an installation'))

    class Meta(object):
        verbose_name = _('Installer')
        verbose_name_plural = _('Installers')

    def __unicode__(self):
        return u'%s %s' % (self.event_user.user.first_name, self.event_user.user.last_name)


class Software(models.Model):
    software_choices = (
        ('OS', _('Operative System')),
        ('AP', _('Application')),
        ('SU', _('Support and Problem Fixing')),
        ('OT', _('Other'))
    )
    name = models.CharField(_('Name'), max_length=200)
    type = models.CharField(_('Type'), choices=software_choices, max_length=200)

    def __unicode__(self):
        return u"%s - %s" % (self.type, self.name)


class Hardware(models.Model):
    hardware_choices = (
        ('MOB', _('Mobile')),
        ('NOTE', _('Notebook')),
        ('NET', _('Netbook')),
        ('TAB', _('Tablet')),
        ('DES', _('Desktop')),
        ('OTH', _('Other'))
    )
    type = models.CharField(_('Type'), choices=hardware_choices, max_length=200)
    manufacturer = models.CharField(_('Manufacturer'), max_length=200, blank=True, null=True)
    model = models.CharField(_('Model'), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.type, self.manufacturer, self.model)


class Room(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), blank=True, null=True)
    name = models.CharField(_('Name'), max_length=200, help_text=_('i.e. Classroom 256'))

    def __unicode__(self):
        return u"%s - %s" % (self.event.name, self.name)

    def get_schedule_info(self):
        return {'id': self.pk, 'title': self.name}

    class Meta(object):
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['name']


class Activity(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    title = models.CharField(_('Title'), max_length=50, blank=False, null=False)
    long_description = models.TextField(_('Long Description'))
    abstract = models.TextField(_('Abstract'), help_text=_('Short idea of the talk (Two or three sentences)'))
    room = models.ForeignKey(Room, verbose_name=_('Room'), blank=True, null=True)
    start_date = models.DateTimeField(_('Start Time'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Time'), blank=True, null=True)
    type = models.CharField(_('Type'), max_length=50, blank=True, null=True)
    speakers_names = models.CharField(_('Speakers Names'), max_length=600,
                                      help_text=_("Comma separated speaker's names"))
    speaker_contact = models.EmailField(_('Speaker Contact'),
                                        help_text=_("Where can whe reach you from the organization team?"))
    labels = models.CharField(_('Labels'), max_length=200,
                              help_text=_('Comma separated tags. i.e. Linux, Free Software, Archlinux'))
    presentation = models.FileField(_('Presentation'), upload_to='talks', blank=True, null=True, help_text=_(
        'Any material you are going to use for the talk (optional, but recommended)'))
    level_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
    )
    level = models.CharField(_('Level'), choices=level_choices, max_length=100,
                             help_text=_("Talk's Technical level"))
    additional_info = models.TextField(_('Additional Info'), blank=True, null=True, help_text=_(
        "Any info you consider relevant for the organizer: i.e. Write here if your activity has any special requirement"))

    status_choices = (
        ('1', _('Proposal')),
        ('2', _('Accepted')),
        ('3', _('Rejected')),
    )

    status = models.CharField(_('Status'), choices=status_choices, max_length=20,
                              help_text=_("Activity proposal status"))

    image = ImageCropField(upload_to='images_thumbnails', verbose_name=_('Image'), blank=True, null=True)
    cropping = ImageRatioField('image', '700x450', size_warning=True, verbose_name=_('Cropping'),
                               help_text=_('The image must be 700x450 px. You can crop it here.'))

    is_dummy = models.BooleanField(_('Is a dummy Activity?'), default=False, help_text=_(
        "A dummy activity is used for example for coffee breaks. We use this to exclude it from the index page and other places"))

    def __cmp__(self, other):
        return -1 if self.start_date.time() < other.start_date.time() else 1

    def __unicode__(self):
        return u"%s - %s" % (self.event, self.title)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('activity_detail', args=(self.event.slug, self.pk))

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

    class Meta(object):
        ordering = ['title']
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class Installation(models.Model):
    hardware = models.ForeignKey(Hardware, verbose_name=_('Hardware'), blank=True, null=True)
    software = models.ForeignKey(Software, verbose_name=_('Software'), blank=True, null=True)
    attendee = models.ForeignKey(Attendee, verbose_name=_('Attendee'),
                                 help_text=_('The owner of the installed hardware'))
    installer = models.ForeignKey(EventUser, verbose_name=_('Installer'), related_name='installed_by', blank=True,
                                  null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True,
                             help_text=_('Any information or trouble you found and consider relevant to document'))

    def __unicode__(self):
        return u"%s, %s, %s" % (self.attendee, self.hardware, self.software)

    class Meta(object):
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')
