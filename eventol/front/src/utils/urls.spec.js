import {
  API_URL,
  EVENTS_API_URL,
  WS_URL,
  EVENTS_WS_URL,
  getTagUrl,
  getWsUrl,
  getEventUrl,
  getApiFullUrl,
  getEventApiUrl,
  getReportQueryParams,
  getReportUrl,
} from './urls';
import {REPORT_REQUIRED_FIELDS} from './constants';

describe('Url utils', () => {
  beforeAll(() => {
    const host = 'localhost:8000';
    global.window = {location: {host}};
  });

  describe('API_URL', () => {
    test('API_URL should be /events/api/', () => {
      expect(API_URL).toEqual('/events/api/');
    });
  });

  describe('EVENTS_API_URL', () => {
    test('EVENTS_API_URL should be /events/api/events/', () => {
      expect(EVENTS_API_URL).toEqual('/events/api/events/');
    });
  });

  describe('WS_URL', () => {
    test('WS_URL should be ws://window.location.host/', () => {
      expect(WS_URL).toEqual(`ws://${window.location.host}/`);
    });
  });

  describe('EVENTS_WS_URL', () => {
    test('EVENTS_WS_URL should be ws://window.location.host/update/events/', () => {
      expect(EVENTS_WS_URL).toEqual(
        `ws://${window.location.host}/updates/events/`
      );
    });
  });

  describe('getTagUrl', () => {
    test('getTagUrl should returns /tags/slug', () => {
      const slug = 'event_slug';
      expect(getTagUrl(slug)).toEqual(`/tags/${slug}`);
    });
  });

  describe('getEventUrl', () => {
    test('getEventUrl should returns /events/slug/', () => {
      const slug = 'event_slug';
      expect(getEventUrl(slug)).toEqual(`/events/${slug}/`);
    });
  });

  describe('getApiFullUrl', () => {
    test('getApiFullUrl should returns /api/event/url', () => {
      const url = '/event_slug?registration=true';
      expect(getApiFullUrl(url)).toEqual(`/api/events/${url}`);
    });
  });

  describe('getWsUrl', () => {
    test('getWsUrl should returns protocol://host/updates/', () => {
      const protocol = 'wss';
      expect(getWsUrl(protocol)).toEqual(
        `${protocol}://${window.location.host}/updates/`
      );
    });

    test('when protocol is undefined, getWsUrl should returns ws://host/updates/', () => {
      expect(getWsUrl()).toEqual(`ws://${window.location.host}/updates/`);
    });
  });

  describe('getEventApiUrl', () => {
    test('getEventApiUrl should returns /api/events/?queryParams', () => {
      const queryParams = 'name=Peter';
      expect(getEventApiUrl(queryParams)).toEqual(
        `/api/events/?${queryParams}`
      );
    });

    test('when queryParams is undefined, getWsUrl should returns /api/events/?', () => {
      expect(getEventApiUrl()).toEqual('/api/events/?');
    });
  });

  describe('getReportQueryParams', () => {
    let page;
    let offset;
    let sorted;
    let pageSize;
    let defaultQueryParams;

    beforeEach(() => {
      pageSize = 10;
      page = 1;
      sorted = [{id: 'name', desc: true}];
      offset = page * pageSize;
      defaultQueryParams = `limit=${pageSize}&offset=${offset}&fields=${REPORT_REQUIRED_FIELDS}`;
    });

    test('should returns query params', () => {
      const queryParams = getReportQueryParams(pageSize, page, sorted);
      expect(queryParams).toEqual(`${defaultQueryParams}&ordering=-name`);
    });

    test('should returns query params without sorted', () => {
      const queryParams = getReportQueryParams(pageSize, page, []);
      expect(queryParams).toEqual(defaultQueryParams);
    });
  });

  describe('getReportUrl', () => {
    let page;
    let offset;
    let sorted;
    let pageSize;
    let defaultQueryParams;

    beforeEach(() => {
      pageSize = 10;
      page = 1;
      sorted = [{id: 'name', desc: true}];
      offset = page * pageSize;
      defaultQueryParams = `limit=${pageSize}&offset=${offset}&fields=${REPORT_REQUIRED_FIELDS}`;
    });

    test('should returns query params', () => {
      const url = getReportUrl(pageSize, page, sorted);
      expect(url).toEqual(`/api/events/?${defaultQueryParams}&ordering=-name`);
    });

    test('should returns query params without sorted', () => {
      const url = getReportUrl(pageSize, page, []);
      expect(url).toEqual(`/api/events/?${defaultQueryParams}`);
    });
  });
});
