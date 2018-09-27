import {
  SET_EVENTS,
  UPDATE_EVENT,
  DELETE_EVENT,
  CREATE_EVENT
} from '../actions/events';
import {getEvent} from '../utils/events';

const initState = {
  events: []
};

const updateEvent = (state, {pk, data}) => {
  return {
    ...state,
    events: [...state.events].map(event => {
      if (event.pk === pk) {
        return getEvent(pk, data);
      }
      return event;
    })
  };
};
const setEvents = (state, events) => ({...state, events});
const createEvent = (state, {pk, data}) => ({...state, events: [...state.events, getEvent(pk, data)]});
const deleteEvent = (state, {pk}) => ({...state, events: [...state.events].filter(event => event.pk !== pk)});

export default (state = initState, action) => {
  switch (action.type) {
  case SET_EVENTS: return setEvents(state, action.events);
  case UPDATE_EVENT: return updateEvent(state, action.event);
  case CREATE_EVENT: return createEvent(state, action.event);
  case DELETE_EVENT: return deleteEvent(state, action.event);
  default: return state;
  }
};
