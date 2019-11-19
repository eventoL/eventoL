import {HOME_REQUIRED_FIELDS} from './constants';


// eslint-disable-next-line prefer-destructuring
export const host = window.location.host;

export const EVENTOL_DOCUMENTATION = 'http://eventol.github.io/eventoL/#/';

export const INDEX_URL = '/';
export const REPORT_URL = '/report';
export const LOGIN_URL = '/accounts/login/';
export const LOGOUT_URL = '/accounts/signup/';
export const PROFILE_URL = '/accounts/profile/';

export const API_URL = '/events/api/';
export const EVENTS_API_URL = `${API_URL}events/`;

export const WS_URL = `ws://${host}/`;
export const EVENTS_WS_URL = `${WS_URL}updates/events/`;

export const getTagUrl = slug => `/tags/${slug}`;
export const getEventUrl = slug => `/events/${slug}/`;
export const getApiFullUrl = url => `/api/events/${url}`;
export const getWsUrl = (protocol = 'ws') => `${protocol}://${host}/updates/`;

const addSlugParams = slug => (slug ? `&tags__slug=${slug}` : '');
export const getMyEventsUrl = slug => `?my_events=true&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getSearchUrl = (searchTerm, slug) => `?search=${searchTerm}&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getRecentEventsUrl = slug => `?ordering=-created_at&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getUpcommingEventsUrl = slug => `?registration_is_open=true&ordering=last_date&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getFeaturedEventsUrl = slug => `?ordering=-attendees_count&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getFinishedEventsUrl = slug => `?registration_is_open=false&ordering=-attendees_count&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;
export const getEventsWithConfirmedScheduleUrl = slug => `?schedule_confirmed=true&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}${addSlugParams(slug)}`;

export const goToUrl = url => {
  window.location.href = url;
};
