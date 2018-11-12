export const API_URL = '/events/api/';
export const EVENTS_API_URL = `${API_URL}events/`;

export const WS_URL = `ws://${window.location.host}/`;
export const EVENTS_WS_URL = `${WS_URL}updates/events/`;

export const getTagUrl = slug => `/tags/${slug}`;

export const goToUrl = url => {
  window.location.href = url;
};
