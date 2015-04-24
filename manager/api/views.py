from django.http import HttpResponse
import json
from voting.models import Vote
from manager.models import Sede, Talk, Attendee, Collaborator, Installer, Installation, TalkProposal


def sede_report(request, sede_url):
    sede = Sede.objects.get(url=sede_url)
    attendees = Attendee.objects.filter(sede=sede)
    talks = Talk.objects.filter(talk_proposal__sede=sede)
    collaborators = Collaborator.objects.filter(sede=sede)
    installers = Installer.objects.filter(collaborator__sede=sede)
    talk_proposals = TalkProposal.objects.filter(sede=sede)
    installations = Installation.objects.filter(attendee__sede=sede)
    votes = Vote.objects.all()
    sede_data = {
        'attendee': {
            'not_confirmed': attendees.filter(assisted=False).count(),
            'confirmed': attendees.filter(assisted=True).count(),
            'is_going_to_install': attendees.filter(is_going_to_install=True).count(),
            'total': attendees.count()
        },
        'talk': {
            'total': talks.count(),
            'talks_for_room': count_by(talks, lambda talk: talk.room.name),
            'talks_for_type': count_by(talks, lambda talk: talk.talk_proposal.type.name),
            'talks_for_level': count_by(talks, lambda talk: talk.talk_proposal.level),
            'talks_not_confirmed': talk_proposals.filter(confirmed=False).count(),
            'talks_confirmed': talk_proposals.filter(confirmed=True).count(),
            'talks_dummys': talk_proposals.filter(dummy_talk=True).count(),
            'votes_for_talk': count_by(votes, lambda vote: TalkProposal.objects.get(
                pk=vote.object_id, sede=sede).title, lambda vote: vote.vote)
        },
        'installation': {
            'total': installations.count(),
            'installation_for_software': count_by(installations, lambda inst: inst.software.name),
            'installation_for_hardware': count_by(installations, lambda inst: inst.hardware.type),
            'installation_for_installer': count_by(installations,
                                                   lambda inst: inst.installer.collaborator.user.username)
        },
        'installer': {
            'total': installers.count(),
            'installers_for_level': count_by(installers, lambda inst: inst.level)
        },
        'staff': get_staff(talk_proposals, installers, collaborators)
    }
    return HttpResponse(json.dumps(sede_data), content_type="application/json")


def count_by(list, getter, increment=None):
    return_dict = {}
    for element in list:
        try:
            field = getter(element)
            if field in return_dict:
                return_dict[field] += increment(element) if increment else 1
            else:
                return_dict[field] = increment(element) if increment else 1
        except Exception:
            pass
    return return_dict


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
