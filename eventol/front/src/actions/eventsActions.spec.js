import {
  setLinks, createLink, updateLink, deleteLink,
  DELETE_LINK, CREATE_LINK, UPDATE_LINK, SET_LINKS
} from './linksActions'

describe('links Actions', () => {
  let link, links, expectDefault;

  beforeEach(() => {
    link = {
      model: 'links.link',
      pk: 1,
      fields: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1
      }
    }
    links = [link]
  });

  describe(SET_LINKS, () => {

    beforeEach(() => {
      expectDefault = {
        type: SET_LINKS,
        links
      }
    })

    test('returns a object', () => {
      const result = setLinks(links)
      expect(result).toBeDefined()
    })

    test('returns correct links', () => {
      const result = setLinks(links)
      expect(result).toEqual(expectDefault)
    })

  })

  describe(UPDATE_LINK, () => {

    beforeEach(() => {
      expectDefault = {
        type: UPDATE_LINK,
        link
      }
    })

    test('returns a object', () => {
      const result = updateLink(link)
      expect(result).toBeDefined()
    })

    test('returns correct links', () => {
      const result = updateLink(link)
      expect(result).toEqual(expectDefault)
    })

  })

  describe(CREATE_LINK, () => {

    beforeEach(() => {
      expectDefault = {
        type: CREATE_LINK,
        link
      }
    })

    test('returns a object', () => {
      const result = createLink(link)
      expect(result).toBeDefined()
    })

    test('returns correct links', () => {
      const result = createLink(link)
      expect(result).toEqual(expectDefault)
    })

  })

  describe(DELETE_LINK, () => {

    beforeEach(() => {
      expectDefault = {
        type: DELETE_LINK,
        link
      }
    })

    test('returns a object', () => {
      const result = deleteLink(link)
      expect(result).toBeDefined()
    })

    test('returns correct links', () => {
      const result = deleteLink(link)
      expect(result).toEqual(expectDefault)
    })

  })

})
