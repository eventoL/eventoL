import {
  SET_EVENTS,
  UPDATE_EVENT,
  DELETE_EVENT,
  CREATE_EVENT
} from '../actions/eventsActions';
import {getEvent} from '../utils/events';

const initState = {
  events: []
};

export default (state = initState, action) => {
  const {events} = state;
  switch (action.type) {
  case SET_EVENTS:
    return {
      ...state,
      events: action.events
    };
  case UPDATE_EVENT:
    return {
      ...state,
      events: events.map(event => {
        if (event.pk === action.event.pk) {
          return getEvent(action.event.pk, action.event.data);
        }
        return event;
      })
    };
  case CREATE_EVENT:
    return {
      ...state,
      events: [...events, getEvent(action.event.pk, action.event.data)]
    };
  case DELETE_EVENT:
    return {
      ...state,
      events: events.filter(event => event.pk !== action.event.pk)
    };
  default:
    return state;
  }
};
//TODO: move case to functions
