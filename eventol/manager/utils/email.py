import cairosvg

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _


def get_ticket_subject(event_name):
    return _('Ticket for {} event').format(event_name)


def get_ticket_body(first_name, last_name, event_name):
    lines = [
        'Hello {0} {1},'.format(first_name, last_name),
        'Here is your ticket for {} event.'.format(event_name),
        'Please remember to print it and bring it with ' +
        'you the day of the event.',
        'Regards, FLISoL {} team.'.format(event_name)
    ]
    return '\n'.join(lines)


def get_installation_subject(first_name, last_name, event_name):
    return _('{0} {1}, thank you for participating in FLISoL {2}'.format(
        first_name, last_name, event_name))


def send_ticket_email(ticket_data, ticket_svg):
    event_name = ticket_data['event'].name
    first_name = ticket_data['first_name']
    last_name = ticket_data['last_name']
    email_to = ticket_data['email']
    ticket_id = ticket_data['ticket'].id
    email = EmailMessage()
    email.subject = get_ticket_subject(event_name)
    email.body = get_ticket_body(
        first_name, last_name, event_name)
    email.to = [email_to]
    ticket_id = str(ticket_id).zfill(12)
    email.attach('Ticket-{}.pdf'.format(ticket_id),
                 cairosvg.svg2pdf(bytestring=ticket_svg),
                 'application/pdf')
    email.send(fail_silently=False)


def send_installation_email(event_name, postinstall_email, attendee):
    email = EmailMultiAlternatives()
    first_name = attendee.first_name
    last_name = attendee.last_name
    email.subject = get_installation_subject(first_name, last_name, event_name)
    email.from_email = postinstall_email.contact_email
    email.body = ''
    email.attach_alternative(postinstall_email.message, "text/html")
    email.to = [attendee.email]
    email.send(fail_silently=False)
