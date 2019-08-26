import { eventReport } from "./report";
export const getEventData = (id, name, tags, report, eventSlug, location) => ({
  id,
  name,
  tags,
  report,
  location,
  event_slug: eventSlug,
});
export const event1Data = getEventData(1, 'event name', { name: 'tag name', slug: 'tag slug' }, eventReport, 'event_slug', ['Capital Federal', 'Pompeya', 'Buenos Aires', 'Argentina']);
export const event2Data = getEventData(2, 'event 2 name', { name: 'tag 2 name', slug: 'tag 2 slug' }, eventReport, 'event_2_slug', ['Capital Federal', 'Monserrat', 'Buenos Aires', 'Argentina']);
export const eventsData = [{ ...event1Data }, { ...event2Data }];
