import {
  API_URL,
  EVENTS_API_URL,
  WS_URL,
  EVENTS_WS_URL,
  getTagUrl,
  getWsUrl,
  getEventUrl,
  getApiFullUrl,
} from './urls';

describe('Url utils', () => {
  beforeAll(() => {
    const host = 'localhost:8000';
    global.window = {location: {host}};
  });

  describe('API_URL', () => {
    it('API_URL should be /events/api/', () => {
      expect(API_URL).toEqual('/events/api/');
    });
  });

  describe('EVENTS_API_URL', () => {
    it('EVENTS_API_URL should be /events/api/events/', () => {
      expect(EVENTS_API_URL).toEqual('/events/api/events/');
    });
  });

  describe('WS_URL', () => {
    it('WS_URL should be ws://window.location.host/', () => {
      expect(WS_URL).toEqual(`ws://${window.location.host}/`);
    });
  });

  describe('EVENTS_WS_URL', () => {
    it('EVENTS_WS_URL should be ws://window.location.host/update/events/', () => {
      expect(EVENTS_WS_URL).toEqual(
        `ws://${window.location.host}/updates/events/`
      );
    });
  });

  describe('getTagUrl', () => {
    it('getTagUrl should returns /tags/slug', () => {
      const slug = 'event_slug';
      expect(getTagUrl(slug)).toEqual(`/tags/${slug}`);
    });
  });

  describe('getEventUrl', () => {
    it('getEventUrl should returns /events/slug/', () => {
      const slug = 'event_slug';
      expect(getEventUrl(slug)).toEqual(`/events/${slug}/`);
    });
  });

  describe('getApiFullUrl', () => {
    it('getApiFullUrl should returns /api/event/url', () => {
      const url = '/event_slug?registration=true';
      expect(getApiFullUrl(url)).toEqual(`/api/events/${url}`);
    });
  });

  describe('getWsUrl', () => {
    it('getWsUrl should returns protocol://host/updates/', () => {
      const protocol = 'wss';
      expect(getWsUrl(protocol)).toEqual(
        `${protocol}://${window.location.host}/updates/`
      );
    });

    it('when protocol is undefined, getWsUrl should returns ws://host/updates/', () => {
      expect(getWsUrl()).toEqual(`ws://${window.location.host}/updates/`);
    });
  });
});
