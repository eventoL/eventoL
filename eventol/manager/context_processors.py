from django.conf import settings


def eventol_settings(request):
    """Add eventol settings"""
    return {
        "PRIVATE_ACTIVITIES": settings.PRIVATE_ACTIVITIES
    }
