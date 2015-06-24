from django.http import HttpResponse
import json
from voting.models import Vote
from manager.api.builder import count_by
from manager.models import Sede, Collaborator, Installer, TalkProposal, Talk, Attendee, Installation
from manager.api import reduces


def sede_report(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    collaborators = Collaborator.objects.filter(sede=sede)
    installers = Installer.objects.filter(collaborator__sede=sede)
    talk_proposals = TalkProposal.objects.filter(sede=sede)
    votes = Vote.objects.all()
    sede_data = {
        'votes_for_talk': count_by(votes, lambda vote: TalkProposal.objects.get(
            pk=vote.object_id, sede=sede).title, lambda vote: vote.vote),
        'staff': get_staff(talk_proposals, installers, collaborators)
    }
    return HttpResponse(json.dumps(sede_data), content_type="application/json")


def sede_full_report(request, sede_url):
    sede = Sede.objects.get(url__iexact=sede_url)
    collaborators = Collaborator.objects.filter(sede=sede)
    installers = Installer.objects.filter(collaborator__sede=sede)
    talks = Talk.objects.filter(talk_proposal__sede=sede)
    talk_proposals = TalkProposal.objects.filter(sede=sede)
    attendees = Attendee.objects.filter(sede=sede)
    sede_data = {
        'talks': [t.talk_proposal.title for t in talks],
        'staff': get_staff(talk_proposals, installers, collaborators),
        'attendees': reduces.attendees(attendees),
        'installations': reduces.installations(Installation.objects.filter(sede=sede))
    }
    return HttpResponse(json.dumps(sede_data), content_type="application/json")


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
