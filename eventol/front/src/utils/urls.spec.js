import {API_URL, EVENTS_API_URL, WS_URL, EVENTS_WS_URL} from './urls.js';

describe('Url utils', () => {
  beforeAll(() => {
    global.window = {location: {host: 'localhost:8000'}};
  });

  describe('API_URL', () => {
    it('should API_URL is /events/api/', () => {
      expect(API_URL).toEqual('/events/api/');
    });
  });

  describe('EVENTS_API_URL', () => {
    it('should EVENTS_API_URL is /events/api/events/', () => {
      expect(EVENTS_API_URL).toEqual('/events/api/events/');
    });
  });

  describe('WS_URL', () => {
    it('should is WS_URL is ws://${window.location.host}/', () => {
      expect(WS_URL).toEqual(`ws://${window.location.host}/`);
    });
  });

  describe('EVENTS_WS_URL', () => {
    it('should is EVENTS_WS_URL is ws://${window.location.host}/update/events/', () => {
      expect(EVENTS_WS_URL).toEqual(`ws://${window.location.host}/updates/events/`);
    });
  });
});
