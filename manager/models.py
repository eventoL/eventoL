from image_cropping import ImageCropField, ImageRatioField
import re
import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _, ugettext_noop as _noop


def validate_url(url):
    if not re.match("^[a-zA-Z0-9-_]+$", url):
        raise ValidationError(_('URL can only contain letters or numbers'))


class Image(models.Model):
    image = ImageCropField(upload_to='images_thumbnails', verbose_name=_('Image'), blank=True, null=True)
    cropping = ImageRatioField('image', '700x450', size_warning=True, verbose_name=_('Cropping'),
                               help_text=_('The image must be 700x450 px. You can crop it here.'))

    def __unicode__(self):
        return self.image.name

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Address(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    address = models.CharField(_('Address'), max_length=200)
    latitude = models.FloatField(_('Latitude'), validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(_('Longitude'), validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __unicode__(self):
        return u"%s (%s-%s)" % (self.name, self.latitude, self.longitude)

    class Meta:
        ordering = ['name']


class Event(models.Model):
    name = models.CharField(_('Event Name'), max_length=200)
    date = models.DateField(_('Date'), help_text=_('When will your event be?'))
    limit_proposal_date = models.DateField(_('Limit Proposals Date'), help_text=_('Limit date to submit talk proposals'))
    slug = models.CharField(_('URL'), max_length=200, help_text=_('For example: flisol-caba'),
                            validators=[validate_url])
    external_url = models.URLField(_('External URL'), blank=True, null=True, default=None, help_text=_('http://www.my-awesome-event.com'))
    email = models.EmailField(verbose_name=_('Email'))
    event_information = RichTextField(verbose_name=_('Event Information'), help_text=_('Event Information HTML'),
                                      blank=True, null=True)
    schedule_confirm = models.BooleanField(_('Schedule Confirm'), default=False)
    place = models.TextField(_('Place')) #TODO: JsonFIELD
    home_image = models.ForeignKey(Image, related_name="eventol_home_image", verbose_name=_noop('Home Image'), blank=True, null=True)
    cover_image = models.ForeignKey(Image, related_name="eventol_cover_image", verbose_name=_noop('Cover Image'), blank=True, null=True)

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        return "/event/" + self.slug + '/'

    @property
    def talk_proposal_is_open(self):
        return self.limit_proposal_date >= datetime.date.today()

    @property
    def registration_is_open(self):
        return self.date >= datetime.date.today()

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_geo_info(self):
        return {
            "lat": self.address.latitude,
            "lon": self.address.longitude,
            "name": self.address.name
        }

    class Meta:
        ordering = ['name']


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')


class ContactType(models.Model):
    """
    For example:
        Name: Facebook
        Icon Class: fa-facebook-square
    """
    name = models.CharField(_('Name'), unique=True, max_length=200)
    icon_class = models.CharField(_('Icon Class'), max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contact Types')


class Contact(models.Model):
    type = models.ForeignKey(ContactType, verbose_name=_('Contact Type'))
    url = models.URLField(_noop('URL'))
    text = models.CharField(_('Text'), max_length=200)
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), related_name='contacts')

    def __unicode__(self):
        return u"%s - %s" % (self.type.name, self.text)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class EventoLUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_noop('Event'), help_text=_('Event you are going to collaborate'))
    assisted = models.BooleanField(_('Assisted'), default=False)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('EventoL User')
        verbose_name_plural = _('EventoL User')


class Collaborator(models.Model):
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)
    assignation = models.CharField(_('Assignation'), max_length=200, blank=True, null=True,
                                   help_text=_('Assignations given to the user (i.e. Talks, Coffee...)'))
    time_availability = models.CharField(_('Time Availability'), max_length=200, blank=True, null=True, help_text=_(
        'Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon"...'))
    phone = models.CharField(_('Phone'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200, blank=True, null=True)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant'))

    class Meta:
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')


class Organizer(models.Model):
    """Event organizer"""
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)

    class Meta:
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')


class Attendee(models.Model):
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant'))

    class Meta:
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')

    def __unicode__(self):
        return u'%s %s' % (self.eventolUser.user.first_name, self.eventolUser.user.last_name)


class InstalationAttendee(models.Model):
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)
    installarion_additional_info = models.TextField(_('Additional Info'), blank=True, null=True,
                                                    help_text=_('i.e. Wath kind of PC are you bringing'))

    class Meta:
        verbose_name = _('Instalation Attendee')
        verbose_name_plural = _('Instalation Attendees')

    def __unicode__(self):
        return u'%s %s' % (self.eventolUser.user.first_name, self.eventolUser.user.last_name)


class Installer(models.Model):
    installer_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
        ('4', _('Super Hacker'))
    )
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)
    level = models.CharField(_('Level'), choices=installer_choices, max_length=200,
                             help_text=_('Linux Knowledge level for an installation'))

    class Meta:
        verbose_name = _('Installer')
        verbose_name_plural = _('Installers')

    def __unicode__(self):
        return u'%s %s' % (self.eventolUser.user.first_name, self.eventolUser.user.last_name)


class Speaker(models.Model):
    eventolUser = models.ForeignKey(EventoLUser, verbose_name=_('EventoL User'), blank=True, null=True)

    class Meta:
        verbose_name = _('Speaker')
        verbose_name_plural = _('Speakers')

userTypes = {
    'Collaborators': Collaborator,
    'Attendees': Attendee,
    'Instalation Attendees': InstalationAttendee,
    'Speakers': Speaker,
    'Intallers': Installer
}


class Software(models.Model):
    software_choices = (
        ('OS', _('Operative System')),
        ('AP', _('Application')),
        ('SU', _('Support and Problem Fixing')),
        ('OT', _('Other'))
    )
    name = models.CharField(_('Name'), max_length=200)
    version = models.CharField(_('Version'), max_length=200)
    type = models.CharField(_('Type'), choices=software_choices, max_length=200)

    def __unicode__(self):
        return u"%s - %s v.%s" % (self.type, self.name, self.version)


class HardwareManufacturer(models.Model):
    name = models.CharField(_('Name'), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Hardware Manufacturer')
        verbose_name_plural = _('Hardware Manufacturers')


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
    manufacturer = models.ForeignKey(HardwareManufacturer, verbose_name=_('Manufacturer'), blank=True, null=True)
    model = models.CharField(_('Model'), max_length=200, blank=True, null=True)
    serial = models.CharField(_('Serial'), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.type, self.manufacturer, self.model)


class Room(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'))
    name = models.CharField(_('Name'), max_length=200, help_text=_('i.e. Classroom 256'))

    def __unicode__(self):
        return u"%s - %s" % (self.event.name, self.name)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        ordering = ['name']


class Activity(models.Model):
    event = models.ForeignKey(Event, verbose_name=_noop('Event'))
    title = models.CharField(_('Title'), max_length=50, blank=True, null=True)
    long_description = models.TextField(_('Long Description'))
    confirmed = models.BooleanField(_('Confirmed'), default=False)
    abstract = models.TextField(_('Abstract'), help_text=_('Short idea of the talk (Two or three sentences)'))
    room = models.ForeignKey(Room, verbose_name=_('Room'), blank=True, null=True)
    start_date = models.DateTimeField(_('Start Time'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Time'), blank=True, null=True)

    def __cmp__(self, other):
        return -1 if self.start_date.time() < other.start_date.time() else 1

    def get_absolute_url(self):
        return "/event/" + self.event.slug + '/activity/detail/activity/' + str(self.id)

    def schedule(self):
        if self.start_date and self.end_date:
            return u"%s - %s" % (self.start_date.strftime("%H:%M"), self.end_date.strftime("%H:%M"))
        return _('Schedule not confirm')

    @classmethod
    def filter_by(cls, queryset, field, value):
        if field == 'event':
            return queryset.filter(event__pk=value)
        return queryset

    def __unicode__(self):
        return u"%s - %s (%s - %s)" % (self.event, self.title,
                                       self.start_date.strftime("%H:%M") if self.start_date else None,
                                       self.end_date.strftime("%H:%M") if self.end_date else None)

    class Meta:
        ordering = ['title']
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class TalkType(models.Model):
    """
    Type of talk. For example: Talk, Workshop, Debate, etc.
    """
    name = models.CharField(_('Name'), max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Talk Type')
        verbose_name_plural = _('Talk Types')


class TalkProposal(models.Model):
    level_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
    )
    activity = models.ForeignKey(Activity, verbose_name=_noop('Activity'), blank=True, null=True)
    type = models.ForeignKey(TalkType, verbose_name=_('Type'))
    image = models.ForeignKey(Image, verbose_name=_noop('Image'), blank=True, null=True)
    confirmed_talk = models.BooleanField(_('Talk Confirmed'), default=False)
    speakers_names = models.CharField(_('Speakers Names'), max_length=600,
                                      help_text=_("Comma separated speaker's names"))
    speakers_email = models.CharField(_('Speakers Emails'), max_length=600,
                                      help_text=_("Comma separated speaker's emails"))
    labels = models.CharField(_('Labels'), max_length=200,
                              help_text=_('Comma separated tags. i.e. Linux, Free Software, Debian'))
    presentation = models.FileField(_('Presentation'), upload_to='talks', blank=True, null=True, help_text=_(
        'Any material you are going to use for the talk (optional, but recommended)'))
    level = models.CharField(_('Level'), choices=level_choices, max_length=100,
                             help_text=_("The talk's Technical level"))

    def get_schedule_info(self):
        return {
            'room': self.activity.room.name,
            'start_date': self.activity.start_date.strftime('%m/%d/%Y %H:%M'),
            'end_date': self.activity.end_date.strftime('%m/%d/%Y %H:%M'),
            'title': self.activity.title,
            'speakers': self.speakers_names,
            'type': self.type.name
        }

    def get_absolute_url(self):
        if self.confirmed_talk:
            return "/event/" + self.activity.event.slug + '/talk/detail/talk/' + str(self.id)
        return "/event/" + self.activity.event.slug + '/talk/detail/proposal/' + str(self.id)

    def __unicode__(self):
        return u"%s: %s" % (self.activity.event, self.activity.title)

    class Meta:
        verbose_name = _('Talk Proposal')
        verbose_name_plural = _('Talk Proposals')


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    activity = models.ForeignKey(Activity, verbose_name=_noop('Activity'))
    user = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return u"%s: %s" % (self.user, self.activity)

    @classmethod
    def filter_by(cls, queryset, field, value):
        if field == 'event':
            return queryset.filter(activity__event__pk=value)
        return queryset

    def save(self, *args, **kwargs):
        """Email when a comment is added."""
        # TODO: Email when a comment is added.
        if "notify" in kwargs:
            del kwargs["notify"]
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Installation(models.Model):
    hardware = models.ForeignKey(Hardware, verbose_name=_('Hardware'), blank=True, null=True)
    software = models.ForeignKey(Software, verbose_name=_('Software'), blank=True, null=True)
    attendee = models.ForeignKey(InstalationAttendee, verbose_name=_('Attendee'),
                                 help_text=_('The owner of the installed hardware'))
    installer = models.ForeignKey(Installer, verbose_name=_('Installer'), related_name='installed_by', blank=True,
                                  null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True,
                             help_text=_('Any information or trouble you found and consider relevant to document'))

    def __unicode__(self):
        return u"%s, %s, %s" % (self.attendee, self.hardware, self.software)

    @classmethod
    def filter_by(cls, queryset, field, value):
        if field == 'event':
            return queryset.filter(attendee__eventolUser__event__pk=value)
        return queryset

    class Meta:
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')


def getUserChoice():
    user_choice = []
    for key in userTypes.keys():
        user_choice.append((key, key))
    return user_choice
