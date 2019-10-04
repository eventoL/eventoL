import {event1} from './__mock__/data';
import {event1Data} from './__mock__/report';

import {getEventUrl} from './urls';
import {getEvent, getSlugParsed, parseEventToItem} from './events';

describe('Event utils', () => {
  describe('getEvent', () => {
    test('should return {pk, fields}', () => {
      const pk = '1';
      const fields = ['name', 'id'];
      expect(getEvent(pk, fields)).toEqual({pk, fields});
    });
  });

  describe('getSlugParsed', () => {
    const slug = 'exAmple-evEnt_slug';

    test('should return Example Event Slug', () => {
      expect(getSlugParsed(slug)).toEqual('Example Event Slug');
    });
  });

  describe('parseEventToItem', () => {
    test('should return event information', () => {
      const event = {...event1, ...event1Data};
      expect(parseEventToItem(event)).toEqual({
        eventSlug: event.event_slug,
        title: event.name,
        attendees: event.attendees_count,
        overview: event.abstract,
        backdrop: event.image,
        place: event.place,
        tags: event.tags,
        key: event.event_slug,
        url: getEventUrl(event.event_slug),
      });
    });
  });
});
