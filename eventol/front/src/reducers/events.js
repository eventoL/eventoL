import _ from 'lodash';
import {
  SET_EVENTS, UPDATE_EVENT,
  DELETE_EVENT, CREATE_EVENT,
} from '../actions/events';
import {getEvent} from '../utils/events';

const initState = {
  events: [],
};

const updateEvent = (state, {pk, data}) => {
  const events = [...state.events];
  const index = _.findIndex(events, {pk});
  events[index] = getEvent(pk, data);
  return {...state, events};
};

const createEvent = (state, {pk, data}) => (
  {...state, events: [...state.events, getEvent(pk, data)]}
);

const deleteEvent = (state, {pk}) => {
  const events = [...state.events];
  _.remove(events, event => event.pk === pk);
  return {...state, events};
};

const setEvents = (state, events) => ({...state, events});

export default (state = initState, action) => {
  switch (action.type){
    case SET_EVENTS: return setEvents(state, action.events);
    case UPDATE_EVENT: return updateEvent(state, action.event);
    case CREATE_EVENT: return createEvent(state, action.event);
    case DELETE_EVENT: return deleteEvent(state, action.event);
    default: return state;
  }
};
