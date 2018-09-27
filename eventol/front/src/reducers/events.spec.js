import eventsReducer from './events';
import {
  SET_EVENTS, UPDATE_EVENT,
  CREATE_EVENT, DELETE_EVENT
} from '../actions/events';

const initState = {
  events: []
};

describe('events Reducer', () => {
  let event, events, event2;

  beforeEach(() => {
    event = {
      model: 'events.event',
      pk: 1,
      data: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1
      }
    };
    event2 = {
      model: 'events.event',
      pk: 2,
      data: {
        name: 'Workshop documentation',
        url: 'https://fedeg.gitlab.io/django-react-workshop',
        pending: true,
        description: '',
        user: 1
      }
    };
    events = [event];
  });

  test('when dispatch ANYTHING event returns a state object', () => {
    const result = eventsReducer(undefined, {type: 'ANYTHING'});
    expect(result).toBeDefined();
  });

  test('when dispatch INIT event returns default', () => {
    const result = eventsReducer(undefined, {type: 'INIT'});
    expect(result).toEqual(initState);
  });

  describe(`when dispatch ${SET_EVENTS}`, () => {
    test('when set events return correct events list', () => {
      const action = {
        type: SET_EVENTS,
        events
      };
      const result = eventsReducer(initState, action);
      expect(result.events).toEqual(events);
    });
  });

  describe(`when dispatch ${UPDATE_EVENT}`, () => {
    test('when update event update original event', () => {
      const action = {
        type: UPDATE_EVENT,
        event: {
          ...event,
          data: {name: 'new name'}
        }
      };
      const expectedEvent = {fields: {name: 'new name'}, pk: 1};
      const result = eventsReducer({events}, action);
      expect(result.events).toEqual([expectedEvent]);
    });

    test('when update event update only original event', () => {
      const action = {
        type: UPDATE_EVENT,
        event: {
          ...event,
          data: {name: 'new name'}
        }
      };
      const expectedEvent = {fields: {name: 'new name'}, pk: 1};
      const result = eventsReducer({events: [event, event2]}, action);
      expect(result.events).toEqual([expectedEvent, event2]);
    });
  });

  describe(`when dispatch ${DELETE_EVENT}`, () => {
    test('when delete event return empty events list', () => {
      const action = {
        type: DELETE_EVENT,
        event
      };
      const result = eventsReducer({events}, action);
      expect(result.events).toEqual([]);
    });
  });

  describe(`when dispatch ${CREATE_EVENT}`, () => {
    test('when create event return correct events list', () => {
      const action = {
        type: CREATE_EVENT,
        event
      };
      const createdEvent = {
        fields: {
          description: '',
          name: 'Gitlab with workshop',
          pending: false,
          url: 'https://gitlab.com/FedeG/django-react-workshop/',
          user: 1
        },
        pk: 1
      };
      const result = eventsReducer({events}, action);
      expect(result.events).toEqual([event, createdEvent]);
    });
  });
});
