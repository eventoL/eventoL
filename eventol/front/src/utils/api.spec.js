import { getUrl } from './api.js';

describe('Api utils', () => {
  let url, params;

  beforeAll(() => {
    url = '/events/api/';
  })

  beforeEach(() => {
    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve([])
      })
    );
    params = {
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': undefined
      },
      method: 'GET'
    }
  });

  afterAll(() => {
    global.fetch.reset();
    global.fetch.restore();
  })

  describe('get', () => {

    it('should API_URL is /events/api/', async () => {
      await getUrl(url);
      expect(global.fetch).toBeCalled();
      expect(global.fetch).lastCalledWith(url, params);
    })

  })

})
