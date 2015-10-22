from django.http import HttpResponse
import json
from voting.models import Vote
from manager.api.builder import count_by
from manager.models import Sede, Collaborator, Installer, TalkProposal


def sede_report(request, event_url, sede_url):
    sede = Sede.objects.get(event__url__iexact=event_url, url__iexact=sede_url)
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
