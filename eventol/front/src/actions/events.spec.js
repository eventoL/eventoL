import {
  setEvents, createEvent, updateEvent, deleteEvent,
  DELETE_EVENT, CREATE_EVENT, UPDATE_EVENT, SET_EVENTS,
} from './events';

describe('events Actions', () => {
  let event, events, expectDefault;

  beforeEach(() => {
    event = {
      model: 'events.event',
      pk: 1,
      fields: {},
    };
    events = [event];
  });

  describe(SET_EVENTS, () => {
    beforeEach(() => {
      expectDefault = {
        type: SET_EVENTS,
        events,
      };
    });

    test('returns a object', () => {
      const result = setEvents(events);
      expect(result).toBeDefined();
    });

    test('returns correct events', () => {
      const result = setEvents(events);
      expect(result).toEqual(expectDefault);
    });
  });

  describe(UPDATE_EVENT, () => {
    beforeEach(() => {
      expectDefault = {
        type: UPDATE_EVENT,
        event,
      };
    });

    test('returns a object', () => {
      const result = updateEvent(event);
      expect(result).toBeDefined();
    });

    test('returns correct events', () => {
      const result = updateEvent(event);
      expect(result).toEqual(expectDefault);
    });
  });

  describe(CREATE_EVENT, () => {
    beforeEach(() => {
      expectDefault = {
        type: CREATE_EVENT,
        event,
      };
    });

    test('returns a object', () => {
      const result = createEvent(event);
      expect(result).toBeDefined();
    });

    test('returns correct events', () => {
      const result = createEvent(event);
      expect(result).toEqual(expectDefault);
    });
  });

  describe(DELETE_EVENT, () => {
    beforeEach(() => {
      expectDefault = {
        type: DELETE_EVENT,
        event,
      };
    });

    test('returns a object', () => {
      const result = deleteEvent(event);
      expect(result).toBeDefined();
    });

    test('returns correct events', () => {
      const result = deleteEvent(event);
      expect(result).toEqual(expectDefault);
    });
  });
});
