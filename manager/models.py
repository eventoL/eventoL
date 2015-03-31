import datetime

from ckeditor.fields import RichTextField
import re
from cities.models import Country, Region, City, District, Place
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext_noop as _noop
from image_cropping import ImageRatioField
from image_cropping.fields import ImageCropField


class Building(Place):
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')


class Sede(models.Model):
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    state = models.ForeignKey(Region, verbose_name=_('State'))
    footer = RichTextField(verbose_name=_('Footer'), help_text=_('Footer HTML'), blank=True, null=True)
    event_information = RichTextField(verbose_name=_('Event Information'), help_text=_('Event Information HTML'),
                                      blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_('City'))
    district = models.ForeignKey(District, verbose_name=_('District'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('Email'))
    name = models.CharField(_('Name'), max_length=200)
    date = models.DateField(_('Date'), help_text=_('Date of the event'))
    limit_proposal_date = models.DateField(_('Limit Proposal Date'), help_text=_('Date Limit of Talk Proposal'))
    place = models.ForeignKey(Building, verbose_name=_('Place'),
                              help_text=_('Specific place (building) where the event is taking place'))
    url = models.CharField(_('URL'), max_length=200, help_text=_('URL for the sede i.e. CABA'), unique=True,
                           db_index=True)

    def get_absolute_url(self):
        return "/sede/" + self.url + '/'

    def __unicode__(self):
        return u"%s / %s / %s - %s" % (self.country, self.state, self.city, self.name)

    def save(self, *args, **kwargs):
        if not re.match("^[a-zA-Z0-9-_]+$", self.url):
            raise ValidationError({'url': _('URL can only contain letters or numbers')})
        super(Sede, self).save(*args, **kwargs)

    def get_geo_info(self):
        return {"lat": self.city.location.y,
                "lon": self.city.location.x,
                "name": self.name,
                "url": reverse('index', args=(self.url,))}

    @property
    def talk_proposal_is_open(self):
        return self.limit_proposal_date > datetime.date.today()


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


class Contact(models.Model):
    type = models.ForeignKey(ContactType, verbose_name=_('Contact Type'))
    url = models.URLField(_noop('URL'))
    text = models.CharField(_('Text'), max_length=200)
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'), related_name='contacts')

    def __unicode__(self):
        return u"%s - %s" % (self.type.name, self.text)


class Attendee(models.Model):
    name = models.CharField(_('First Name'), max_length=200, blank=True, null=True)
    surname = models.CharField(_('Last Name'), max_length=200, blank=True, null=True)
    nickname = models.CharField(_('Nickname'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=200)
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'), help_text=_('Sede you are going to attend'))
    assisted = models.BooleanField(_('Assisted'), default=False)
    is_going_to_install = models.BooleanField(_('Is going to install?'), default=False,
                                              help_text=_('Are you going to bring a PC for installing it?'))
    additional_info = models.TextField(_('Additional Info'), blank=True, null=True,
                                       help_text=_('i.e. Wath kind of PC are you bringing'))

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')
        unique_together = ('email', 'sede',)


class Collaborator(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), blank=True, null=True)
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'), help_text=_('Sede you are going to collaborate'))
    phone = models.CharField(_('Phone'), max_length=200, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=200, blank=True, null=True)
    assisted = models.BooleanField(_('Assisted'), default=False)
    is_coordinator = models.BooleanField(_('Is Coordinator'), default=False,
                                         help_text=_('The user is the coordinator of the sede?'))
    assignation = models.CharField(_('Assignation'), max_length=200, blank=True, null=True,
                                   help_text=_('Assignations given to the user (i.e. Talks, Coffee...)'))
    additional_info = models.CharField(_('Additional Info'), max_length=200, blank=True, null=True,
                                       help_text=_('Any additional info you consider relevant'))
    time_availability = models.CharField(_('Time Availability'), max_length=200, blank=True, null=True, help_text=_(
        'Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon"...'))

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('Collaborator')
        verbose_name_plural = _('Collaborators')


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


class Installer(models.Model):
    collaborator = models.OneToOneField(Collaborator, verbose_name=_('Collaborator'), blank=True, null=True)
    installer_choices = (
        ('1', _('Beginner')),
        ('2', _('Medium')),
        ('3', _('Advanced')),
        ('4', _('Super Hacker'))
    )
    level = models.CharField(_('Level'), choices=installer_choices, max_length=200,
                             help_text=_('Linux Knowledge level for an installation'))
    software = models.ManyToManyField(Software, verbose_name=_('Software'), blank=True, null=True, help_text=_(
        'Select all the software you can install. Hold Ctrl key to select many'))

    def __unicode__(self):
        return str(self.collaborator.user)

    class Meta:
        verbose_name = _('Installer')
        verbose_name_plural = _('Installers')


class Installation(models.Model):
    hardware = models.ForeignKey(Hardware, verbose_name=_('Hardware'), blank=True, null=True)
    software = models.ForeignKey(Software, verbose_name=_('Software'), blank=True, null=True)
    attendee = models.ForeignKey(Attendee, verbose_name=_('Attendee'),
                                 help_text=_('The owner of the installed hardware'))
    installer = models.ForeignKey(Installer, verbose_name=_('Installer'), related_name='installed_by', blank=True,
                                  null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True,
                             help_text=_('Any information or trouble you found and consider relevant to document'))

    def __unicode__(self):
        return u"%s, %s, %s" % (self.attendee, self.hardware, self.software)

    class Meta:
        verbose_name = _('Installation')
        verbose_name_plural = _('Installations')


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
    title = models.CharField(_('Title'), max_length=600)
    type = models.ForeignKey(TalkType, verbose_name=_('Type'))
    long_description = models.TextField(_('Long Description'))
    confirmed = models.BooleanField(_('Confirmed'), default=False)
    dummy_talk = models.BooleanField(_('Dummy Talk?'), default=False)
    abstract = models.TextField(_('Abstract'), help_text=_('Short idea of the talk (Two or three sentences)'))
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'), help_text=_('Sede you are proposing the talk to'),
                             related_name='talk_proposals')
    speakers_names = models.CharField(_('Speakers Names'), max_length=600,
                                      help_text=_("Comma separated speaker's names"))
    speakers_email = models.CharField(_('Speakers Emails'), max_length=600,
                                      help_text=_("Comma separated speaker's emails"))
    labels = models.CharField(_('Labels'), max_length=200,
                              help_text=_('Comma separated tags. i.e. Linux, Free Software, Debian'))
    presentation = models.FileField(_('Presentation'), upload_to='talks', blank=True, null=True, help_text=_(
        'Any material you are going to use for the talk (optional, but recommended)'))
    home_image = ImageCropField(upload_to='talks_thumbnails', verbose_name=_('Home Page Image'), blank=True, null=True,
                                help_text=_(
                                    'Image that is going to appear in the home page of this web for promoting the '
                                    'talk (optional)'))
    cropping = ImageRatioField('home_image', '700x450', size_warning=True, verbose_name=_('Cropping'),
                               help_text=_('The image must be 700x450 px. You can crop it here.'))
    level = models.CharField(_('Level'), choices=level_choices, max_length=100,
                             help_text=_("The talk's Technical level"), default='Beginner')

    def get_absolute_url(self):
        return "/sede/" + self.sede.url + '/talk/detail/proposal/' + str(self.id)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Talk Proposal')
        verbose_name_plural = _('Talk Proposals')


class Room(models.Model):
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'))
    name = models.CharField(_('Name'), max_length=200, help_text=_('i.e. Classroom 256'))
    for_type = models.ForeignKey(TalkType, verbose_name=_('For talk type'),
                                 help_text=_('The type of talk the room is going to be used for.'))

    def __unicode__(self):
        return u"%s - %s" % (self.sede.name, self.name)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')


class Talk(models.Model):
    talk_proposal = models.OneToOneField(TalkProposal, verbose_name=_('TalkProposal'), blank=True, null=True)
    room = models.ForeignKey(Room, verbose_name=_('Room'))
    speakers = models.ManyToManyField(Collaborator, related_name='speakers', verbose_name=_('Speakers'))
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))

    def get_absolute_url(self):
        return "/sede/" + self.talk_proposal.sede.url + '/talk/detail/talk/' + str(self.id)

    def __unicode__(self):
        return u"%s - %s (%s - %s)" % (self.talk_proposal.sede.name, self.talk_proposal.title,
                                       self.start_date.strftime("%H:%M"), self.end_date.strftime("%H:%M"))

    class Meta:
        verbose_name = _('Talk')
        verbose_name_plural = _('Talks')


class EventInfo(models.Model):
    sede = models.ForeignKey(Sede, verbose_name=_noop('Sede'))
    html = models.TextField()

    class Meta:
        verbose_name = _('Event Info')
        verbose_name_plural = _('Envent Info (s)')


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=60)
    body = models.TextField()
    proposal = models.ForeignKey(TalkProposal)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode("%s: %s (%s)" % (self.user, self.proposal, self.created.strftime('%Y-%m-%d %H:%M')))

    def save(self, *args, **kwargs):
        """Email when a comment is added."""

        # TODO: Email when a comment is added.

        if "notify" in kwargs:
            del kwargs["notify"]
        super(Comment, self).save(*args, **kwargs)
