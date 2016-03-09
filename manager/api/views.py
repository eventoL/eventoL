import json

from django.http import HttpResponse
from voting.models import Vote
from manager.api.rest.builder import count_by
from manager.models import Event, Collaborator, Installer, TalkProposal, Talk, Attendee, Installation
from manager.api.rest import reduces


def event_report(request, event_url):
    event = Event.objects.get(url__iexact=event_url)
    collaborators = Collaborator.objects.filter(event=event)
    installers = Installer.objects.filter(collaborator__event=event)
    talk_proposals = TalkProposal.objects.filter(event=event)
    votes = Vote.objects.all()
    event_data = {
        'votes_for_talk': count_by(votes, lambda vote: TalkProposal.objects.get(
            pk=vote.object_id, event=event).title, lambda vote: vote.vote),
        'staff': get_staff(talk_proposals, installers, collaborators)
    }
    return HttpResponse(json.dumps(event_data), content_type="application/json")


def event_full_report(request, event_url):
    event = Event.objects.get(url__iexact=event_url)
    collaborators = Collaborator.objects.filter(event=event)
    installers = Installer.objects.filter(collaborator__event=event)
    talks = Talk.objects.filter(talk_proposal__event=event)
    talk_proposals = TalkProposal.objects.filter(event=event)
    attendees = Attendee.objects.filter(event=event)
    event_data = {
        'talks': [t.talk_proposal.title for t in talks],
        'staff': get_staff(talk_proposals, installers, collaborators),
        'attendees': reduces.attendees(attendees),
        'installations': reduces.installations(Installation.objects.filter(attendee__event=event))
    }
    return HttpResponse(json.dumps(event_data), content_type="application/json")


def get_staff(talks, installers, collaborators):
    staff_collaborators, speakers = [], []
    for talk in talks:
        speakers += [speaker.strip() for speaker in talk.speakers_names.split(',')]
    installers = [installer.collaborator.user.username for installer in installers
                  if installer.collaborator.user.username not in speakers]
    for collaborator in collaborators:
        if collaborator.user.username not in speakers:
            if collaborator.user.username not in installers:
                staff_collaborators.append(collaborator.user.username)
    return {'collaborators': len(staff_collaborators), 'installers': len(installers), 'speakers': len(speakers)}
