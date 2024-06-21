import _ from 'lodash';

jest.mock('./logger', () => ({
  error: jest.fn(),
  warning: jest.fn(),
}));

jest.mock('./urls', () => ({
  getReportUrl: jest.fn(() => 'REPORT_URL'),
}));

import Logger from './logger';
import {getReportUrl} from './urls';
import {
  getUrl,
  postUrl,
  addQueryString,
  genericFetch,
  loadReports,
} from './api';

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
        ok: true,
        json: () => Promise.resolve([]),
      })
    );
  });

  const getLastCall = () => _.last(global.fetch.mock.calls);

  afterAll(() => {
    global.fetch.reset();
    global.fetch.restore();
  });

  describe('genericFetch', () => {
    test('should get a correct url', async () => {
      await genericFetch(url);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url);
    });

    test('should add a queryString', async () => {
      await genericFetch(url, {test: true, name: 'Peter'});
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(`${url}?test=true&name=Peter`);
    });

    test('should add a queryString and params', async () => {
      const params = {Accept: 'application/json'};
      await genericFetch(url, {name: 'Peter'}, params);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(`${url}?name=Peter`);
      expect(getLastCall()[1]).toBe(params);
    });

    test('should show error log when res is not ok', async () => {
      const res = {
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      };
      global.fetch = jest.fn().mockImplementation(() => Promise.resolve(res));

      await genericFetch(url);
      expect(Logger.error).toBeCalled();
      expect(Logger.error).toBeCalledWith(
        'There has been an error',
        res.status,
        res.statusText
      );
    });

    test('should show redirect to / in 403 response', async () => {
      const res = {
        ok: false,
        status: 403,
        statusText: 'Forbidden Error',
      };
      global.fetch = jest.fn().mockImplementation(() => Promise.resolve(res));

      await genericFetch(url);
      expect(Logger.warning).toBeCalled();
      expect(Logger.warning).toBeCalledWith(
        'Redirect to /',
        res.status,
        res.statusText
      );
    });
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

  describe('loadReports', () => {
    let page;
    let sorted;
    let pageSize;

    beforeEach(() => {
      pageSize = 10;
      page = 1;
      sorted = {id: 'name', desc: true};
    });

    test('should call getReportUrl with correct params', () => {
      loadReports(pageSize, page, sorted);
      expect(getReportUrl).toBeCalled();
      expect(getReportUrl).toBeCalledWith(pageSize, page, sorted);
    });

    test('should call fetch with correct params', () => {
      loadReports(pageSize, page, sorted);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(getReportUrl(pageSize, page, sorted));
    });
  });
});
