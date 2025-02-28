from django.db import connection


def get_custom_fields(event, data):
    if not event.customForm:
        return {}
    slugs = list(event.customForm.fields.values_list('slug', flat=True))
    customFields = {}
    for slug in slugs:
        customFields[slug] = data[slug] or None
    return customFields


USE_POSTGRES = connection.vendor == 'postgresql'
