import {
  SET_EVENTS, UPDATE_EVENT,
  DELETE_EVENT, CREATE_EVENT,
} from '../actions/events';

const initState = {
  events: {
    events: [],
  },
};

describe('Events store', () => {
  let store, event, events;

  beforeEach(() => {
    /* eslint-disable-next-line global-require */
    const getStore = require('./index').default;
    store = getStore();
    event = {
      model: 'events.event',
      pk: 1,
      data: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1,
      },
    };
    events = [event];
  });

  test('returns a state object', () => {
    const result = store.getState();
    expect(result).toBeDefined();
  });

  test('returns default', () => {
    const result = store.getState();
    expect(result).toEqual(initState);
  });

  describe('events reducers', () => {
    test('when dispatch SET_EVENTS returns correct state', () => {
      const expectData = {events};
      store.dispatch({type: SET_EVENTS, events});
      expect(store.getState().events).toEqual(expectData);
    });

    test('when dispatch UPDATE_EVENT returns correct state', () => {
      const expectedEvent = {fields: {name: 'new name'}, pk: 1};
      const expectData = {events: [expectedEvent]};
      store.dispatch({type: SET_EVENTS, events});
      store.dispatch({
        type: UPDATE_EVENT,
        event: {
          ...event,
          data: {name: 'new name'},
        },
      });
      expect(store.getState().events).toEqual(expectData);
    });

    test('when dispatch DELETE_EVENT returns correct state', () => {
      const expectData = {events: []};
      store.dispatch({type: SET_EVENTS, events});
      store.dispatch({type: DELETE_EVENT, event});
      expect(store.getState().events).toEqual(expectData);
    });

    test('when dispatch CREATE_EVENT returns correct state', () => {
      const createdEvent = {
        fields: {
          description: '',
          name: 'Gitlab with workshop',
          pending: false,
          url: 'https://gitlab.com/FedeG/django-react-workshop/',
          user: 1,
        },
        pk: 1,
      };
      const expectData = {events: [event, createdEvent]};
      store.dispatch({type: SET_EVENTS, events});
      store.dispatch({type: CREATE_EVENT, event});
      expect(store.getState().events).toEqual(expectData);
    });
  });
});
