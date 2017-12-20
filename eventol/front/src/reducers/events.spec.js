import linksReducer from './links'

const initState = {
  links: []
}

describe('links Reducer', () => {
  let link, links, link2;

  beforeEach(() => {
    link = {
      model: 'links.link',
      pk: 1,
      data: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1
      }
    }
    link2 = {
      model: 'links.link',
      pk: 2,
      data: {
        name: 'Workshop documentation',
        url: 'https://fedeg.gitlab.io/django-react-workshop',
        pending: true,
        description: '',
        user: 1
      }
    }
    links = [link]
  });

  test('when dispatch ANYTHING event returns a state object', () => {
    const result = linksReducer(undefined, {type: 'ANYTHING'});
    expect(result).toBeDefined();
  });

  test('when dispatch INIT event returns default', () => {
    const result = linksReducer(undefined, {type: 'INIT'});
    expect(result).toEqual(initState);
  });

  describe('when dispatch SET_LINKS', () => {

    test('when set links return correct links list', () => {
      const action = {
        type: 'SET_LINKS',
        links
      }
      const result = linksReducer(initState, action);
      expect(result.links).toEqual(links);
    });

  });

  describe('when dispatch UPDATE_LINK', () => {

    test('when update link update original link', () => {
      const action = {
        type: 'UPDATE_LINK',
        link: {
          ...link,
          data: { name: 'new name' },
        }
      }
      const expectedLink = {fields: {name: 'new name'}, pk: 1};
      const result = linksReducer({links}, action);
      expect(result.links).toEqual([expectedLink]);
    });

    test('when update link update only original link', () => {
      const action = {
        type: 'UPDATE_LINK',
        link: {
          ...link,
          data: { name: 'new name' },
        }
      }
      const expectedLink = {fields: {name: 'new name'}, pk: 1};
      const result = linksReducer({links: [link, link2]}, action);
      expect(result.links).toEqual([expectedLink, link2]);
    });

  });

  describe('when dispatch DELETE_LINK', () => {

    test('when delete link return empty links list', () => {
      const action = {
        type: 'DELETE_LINK',
        link
      }
      const result = linksReducer({links}, action);
      expect(result.links).toEqual([]);
    });

  });

  describe('when dispatch CREATE_LINK', () => {

    test('when create link return correct links list', () => {
      const action = {
        type: 'CREATE_LINK',
        link
      }
      const createdLink = {
       fields: {
          description: '',
          name: 'Gitlab with workshop',
          pending: false,
          url: 'https://gitlab.com/FedeG/django-react-workshop/',
          user: 1,
        },
        pk: 1,
      }
      const result = linksReducer({links}, action);
      expect(result.links).toEqual([link, createdLink]);
    });

  });

})
