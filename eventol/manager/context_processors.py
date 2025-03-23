from django.conf import settings

from manager.models import EventolSetting


def eventol_settings(request):
    """Add eventol settings"""
    return {
        "PRIVATE_ACTIVITIES": settings.PRIVATE_ACTIVITIES,
        "EVENTOL_SETTINGS": EventolSetting.load(),
    }
