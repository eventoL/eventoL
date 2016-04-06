import json

from django.http import HttpResponse
from voting.models import Vote
from manager.api.rest.reduces import count_by
from manager.models import Event, Activity, Collaborator, Installer, TalkProposal,\
    Attendee, Installation, Speaker, NonRegisteredAttendee, Organizer, InstallationAttendee
from manager.api.rest import reduces


def event_report(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    collaborators = Collaborator.objects.filter(eventUser__event=event)
    installers = Installer.objects.filter(eventUser__event=event)
    speakers = Speaker.objects.filter(eventUser__event=event)
    organizers = Organizer.objects.filter(eventUser__event=event)
    talk_proposals = TalkProposal.objects.filter(activity__event=event)
    votes = Vote.objects.all()
    event_data = {
        'votes_for_talk': count_by(votes,
                                   lambda vote: TalkProposal.objects.get(pk=vote.object_id, event=event).activity.title,
                                   lambda vote: vote.vote),
        'staff': get_staff(talk_proposals, collaborators, installers, speakers, organizers)
    }
    return HttpResponse(json.dumps(event_data), content_type="application/json")


def event_full_report(request, event_slug):
    event = Event.objects.get(slug__iexact=event_slug)
    collaborators = Collaborator.objects.filter(eventUser__event=event)
    installers = Installer.objects.filter(eventUser__event=event)
    speakers = Speaker.objects.filter(eventUser__event=event)
    organizers = Organizer.objects.filter(eventUser__event=event)
    attendees = Attendee.objects.filter(eventUser__event=event)
    installation_attendees = InstallationAttendee.objects.filter(eventUser__event=event)
    activities, talk_proposals = [], []
    for activity in Activity.objects.filter(event=event):
        talk_proposal = TalkProposal.objects.filter(activity=activity).first()
        if talk_proposal:
            talk_proposals.append(talk_proposal)
        activities.append(activity)
    nr_attendees = []
    for attendee in NonRegisteredAttendee.objects.all():
        if attendee.eventuser_set.first():
            nr_attendees.append(attendee)
    event_data = {
        'talks': [t.activity.title for t in talk_proposals],
        'staff': get_staff(talk_proposals, collaborators, installers, speakers, organizers),
        'attendees': reduces.attendees(attendees),
        'non_registered_attendees': len(nr_attendees),
        'installation_attendees': len(installation_attendees),
        'activities': [a.title for a in activities],
        'installations': reduces.installations(Installation.objects.filter(attendee__event=event))
    }
    return HttpResponse(json.dumps(event_data), content_type="application/json")


def get_staff(talks, collaborators, installers, speakers, organizers):
    speakers_list = []
    for talk in talks:
        speakers_list += [speaker.strip() for speaker in talk.speakers_names.split(',')]
    return {
        'collaborators': len(collaborators),
        'installers': len(installers),
        'speakers': len(speakers)+len(speakers_list),
        'organizers': len(organizers)
    }
