export const SET_EVENTS = 'SET_EVENTS';
export const UPDATE_EVENT = 'UPDATE_EVENT';
export const DELETE_EVENT = 'DELETE_EVENT';
export const CREATE_EVENT = 'CREATE_EVENT';

export const setEvents = events => ({type: SET_EVENTS, events});
export const updateEvent = event => ({type: UPDATE_EVENT, event});
export const deleteEvent = event => ({type: DELETE_EVENT, event});
export const createEvent = event => ({type: CREATE_EVENT, event});

const eventsActions = {
  setEvents,
  createEvent,
  updateEvent,
  deleteEvent,
  DELETE_EVENT,
  CREATE_EVENT,
  UPDATE_EVENT,
  SET_EVENTS,
};
export default eventsActions;
