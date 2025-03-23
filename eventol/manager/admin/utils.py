# pylint: disable=too-many-return-statements

from manager.models import Organizer


def filter_model_queryset_by_user(user, model):
    if user.is_superuser:
        return model.objects.all()

    model_name = model._meta.model_name
    organizers = Organizer.objects.filter(event_user__user=user)
    events = [organizer.event_user.event for organizer in organizers.iterator()]

    if model_name == "event":
        events_ids = [event.id for event in events]
        return model.objects.filter(id__in=events_ids).distinct()

    if model_name in [
        "activity",
        "attendee",
        "contact",
        "contactmessage",
        "event_date",
        "eventdate",
        "event_user",
        "eventuser",
        "installationmessage",
        "room",
    ]:
        return model.objects.filter(event__in=events).distinct()

    if model_name in ["collaborator", "installer", "organizer", "reviewer"]:
        return model.objects.filter(event_user__event__in=events).distinct()

    if model_name == "user":
        return model.objects.filter(id=user.id)

    if model_name == "installation":
        return model.objects.filter(installer__event__in=events).distinct()

    if model_name in [
        "activity_type",
        "activitytype",
        "contacttype",
        "customform",
        "hardware",
        "software",
        "ticket",
        "type",
    ]:
        return model.objects.all().distinct()

    return model.objects.none()
