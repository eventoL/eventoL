from manager.models import InstallationAttendee, NonRegisteredAttendee, EventUser


def basic_reduce(queryset):
    return {'total': queryset.count()}


def count_if(elements, conditions):
    count = 0
    for element in elements:
        try:
            if all(element[key] == value for key, value in conditions.items()):
                count += 1
        except Exception:
            pass
    return count


def count_by(elements, getter, increment=None):
    return_dict = {}
    for element in elements:
        try:
            field = getter(element)
            if field in return_dict:
                return_dict[field] += increment(element) if increment else 1
            else:
                return_dict[field] = increment(element) if increment else 1
        except Exception:
            pass
    return return_dict


def proposals(proposals_list):
    data = {
        'talks_not_confirmed': proposals_list.filter(confirmed_talk=False).count(),
        'talks_confirmed': proposals_list.filter(confirmed_talk=True).count(),
        'total': proposals_list.count()
    }
    return data


def attendees(attendees_list):
    data = {
        'not_confirmed': attendees_list.filter(eventUser__assisted=False).count(),
        'confirmed': attendees_list.filter(eventUser__assisted=True).count(),
        'total': attendees_list.count()
    }
    return data


def installations(installations_list):
    data = {
        'total': installations_list.count(),
        'installation_for_software': count_by(installations_list, lambda inst: inst.software.name),
        'installation_for_hardware': count_by(installations_list, lambda inst: inst.hardware.type),
        'installation_for_installer': count_by(installations_list, lambda inst: inst.installer.collaborator.user.username)
    }
    return data


def installers(installers_list):
    data = {
        'total': installers_list.count(),
        'installers_for_level': count_by(installers_list, lambda inst: inst.level)
    }
    return data
