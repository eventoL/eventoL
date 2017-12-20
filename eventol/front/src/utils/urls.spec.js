import { API_URL, LINKS_API_URL, WS_URL, LINKS_WS_URL } from './urls.js';

describe('Url utils', () => {

  beforeAll(() => {
    global.window = {location: {host: 'localhost:8000'}};
  })

  describe('API_URL', () => {

    it('should API_URL is /links/api/', () => {
      expect(API_URL).toEqual('/links/api/');
    })

  })

  describe('LINKS_API_URL', () => {

    it('should LINKS_API_URL is /links/api/links/', () => {
      expect(LINKS_API_URL).toEqual('/links/api/links/');
    })

  })

  describe('WS_URL', () => {

    it('should is WS_URL is ws://${window.location.host}/', () => {
      expect(WS_URL).toEqual(`ws://${window.location.host}/`);
    })

  })

  describe('LINKS_WS_URL', () => {

    it('should is LINKS_WS_URL is ws://${window.location.host}/update/links/', () => {
      expect(LINKS_WS_URL).toEqual(`ws://${window.location.host}/updates/links/`);
    })

  })

})
