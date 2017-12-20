import { getUrl } from './api.js';

describe('Api utils', () => {
  let url;

  beforeAll(() => {
    url = '/links/api/';
  })

  beforeEach(() => {
    global.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve({
        json: () => Promise.resolve([])
      })
    );
  });

  afterAll(() => {
    global.fetch.reset();
    global.fetch.restore();
  })

  describe('get', () => {

    it('should API_URL is /links/api/', async () => {
      await getUrl(url);
      expect(global.fetch).toBeCalled();
      expect(global.fetch).lastCalledWith(url);
    })

  })

})
