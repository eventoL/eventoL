import logging

logger = logging.getLogger('eventol')


def count_by(elements, getter, increment=None):
    return_dict = {}
    for element in elements:
        try:
            field = str(getter(element))
            if field in return_dict:
                return_dict[field] += increment(element) if increment else 1
            else:
                return_dict[field] = increment(element) if increment else 1
        except Exception as error:
            logger.error(error)
    return return_dict
