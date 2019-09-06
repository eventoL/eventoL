import _ from 'lodash';

import {getUrl, postUrl, addQueryString} from './api';

describe('Api utils', () => {
  let url;
  let data;
  let body;
  let query;

  beforeAll(() => {
    url = '/api/';
    data = {user: 'example', password: 'secret'};
    body = JSON.stringify(data);
    query = {
      slug: 'event_slug',
      registration: true,
    };
  });

  beforeEach(() => {
    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve([]),
      })
    );
  });

  function getLastCall() {
    return _.last(global.fetch.mock.calls);
  }

  afterAll(() => {
    global.fetch.reset();
    global.fetch.restore();
  });

  describe('get', () => {
    test('should get a correct url', async () => {
      await getUrl(url);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url);
    });

    test('should add a queryString', async () => {
      await getUrl(url, {test: true, name: 'Peter'});
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(`${url}?test=true&name=Peter`);
    });
  });

  describe('post', () => {
    test('should post to correct url', async () => {
      await postUrl(url, data);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url);
      expect(getLastCall()[1].body).toBe(body);
    });

    test('should add a queryString', async () => {
      await postUrl(url, data, {test: true, name: 'Peter'});
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(`${url}?test=true&name=Peter`);
    });
  });

  describe('addQueryString', () => {
    test('should return url with querystring', () => {
      const urlWithQueryString = addQueryString(url, query);
      expect(urlWithQueryString).toEqual(
        '/api/?slug=event_slug&registration=true'
      );
    });

    test('when empty querystring, should return url', () => {
      const urlWithQueryString = addQueryString(url);
      expect(urlWithQueryString).toEqual('/api/');
    });
  });
});
