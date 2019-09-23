import {getEventUrl} from './urls';
import {LOGO_LANDING_DEFAULT} from './constants';

export const getEvent = (pk, fields) => ({pk, fields});
export const getSlugParsed = slug =>
  slug
    .toLowerCase()
    .replace(/[-_]/g, ' ')
    .split(' ')
    .map(word => word.replace(word[0], word[0].toUpperCase()))
    .join(' ');

export const parseEventToItem = ({
  tags,
  place,
  image,
  name: title,
  attendees_count: attendees,
  abstract: overview,
  event_slug: eventSlug,
}) => {
  let backdrop = image;
  if (image) {
    backdrop = new URL(image).pathname;
  }
  return {
    eventSlug,
    title,
    attendees,
    overview,
    backdrop,
    place,
    tags,
    key: eventSlug,
    url: getEventUrl(eventSlug),
  };
};

export const emptyEventItem = {
  key: 'not_found',
  title: gettext('Event not found'),
  overview: gettext('No Event found in your search'),
  backdrop: LOGO_LANDING_DEFAULT,
};
