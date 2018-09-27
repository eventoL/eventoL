import {getUrl, postUrl} from './api.js';

describe('Api utils', () => {
  let url, data, body;

  beforeAll(() => {
    url = '/api/';
    data = {user: 'example', password: 'secret'};
    body = JSON.stringify(data);
  });

  beforeEach(() => {
    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve([])
      })
    );
  });

  function getLastCall() {
    return global.fetch.mock.calls[global.fetch.mock.calls.length - 1];
  }

  afterAll(() => {
    global.fetch.reset();
    global.fetch.restore();
  });

  describe('get', () => {
    it('should get a correct url', async () => {
      await getUrl(url);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url);
    });

    it('should add a queryString', async () => {
      await getUrl(url, {test: true, name: 'Peter'});
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url + '?test=true&name=Peter');
    });
  });

  describe('post', () => {
    it('should post to correct url', async () => {
      await postUrl(url, data);
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url);
      expect(getLastCall()[1].body).toBe(body);
    });

    it('should add a queryString', async () => {
      await postUrl(url, data, {test: true, name: 'Peter'});
      expect(global.fetch).toBeCalled();
      expect(getLastCall()[0]).toBe(url + '?test=true&name=Peter');
    });
  });
});
