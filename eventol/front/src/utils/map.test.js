jest.mock('./logger', () => ({error: jest.fn()}));
import Logger from './logger';

import {MAP_SETTINGS, MAP_LAYER} from './constants';
import {getMapId, loadMap} from './map';

import {event1} from './__mock__/data';

describe('Map utils', () => {
  const mapId = 'mapId';

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('getMapId', () => {
    test('getMapId should return <sliderId><eventSlug>', () => {
      expect(getMapId(event1.eventSlug, event1.id)).toEqual('1event1slug');
    });
  });

  describe('loadMap', () => {
    test('should call L.map', () => {
      loadMap(event1.place, mapId);

      expect(L.map).toBeCalled();
      expect(L.map).toBeCalledWith(mapId, MAP_SETTINGS);
    });

    test('should call L.tileLayer', () => {
      loadMap(event1.place, mapId);

      expect(L.tileLayer).toBeCalled();
      expect(L.tileLayer).toBeCalledWith(MAP_LAYER, {attribution: ''});
    });

    test('should call L.marker', () => {
      const {geometry} = JSON.parse(event1.place);
      const eventLat = geometry.location.lat;
      const eventLon = geometry.location.lng;

      loadMap(event1.place, mapId);

      expect(L.marker).toBeCalled();
      expect(L.marker).toBeCalledWith([eventLat, eventLon]);
    });

    test('should call Logger.error when the JSON is not valid ', () => {
      loadMap('NOT VALID JSON', mapId);

      expect(Logger.error).toBeCalled();
      expect(Logger.error.mock.calls[0][0]).toBeInstanceOf(SyntaxError);
      expect(Logger.error.mock.calls[0][0].message).toEqual(
        'Unexpected token N in JSON at position 0'
      );
    });
  });
});
