import {MAP_SETTINGS, MAP_LAYER} from './constants';
import {getMapId, loadMap} from './map';

import {event1} from './__mock__/data';

describe('Map utils', () => {
  describe('getMapId', () => {
    test('getMapId should return <sliderId><eventSlug>', () => {
      expect(getMapId(event1.eventSlug, event1.id)).toEqual('1event1slug');
    });
  });

  describe('loadMap', () => {
    test('should call L.map', () => {
      const mapId = 'mapId';

      loadMap(event1.place, mapId);

      expect(L.map).toBeCalled();
      expect(L.map).toBeCalledWith(mapId, MAP_SETTINGS);
    });

    test('should call L.tileLayer', () => {
      const mapId = 'mapId';

      loadMap(event1.place, mapId);

      expect(L.tileLayer).toBeCalled();
      expect(L.tileLayer).toBeCalledWith(MAP_LAYER, {attribution: ''});
    });

    test('should call L.marker', () => {
      const {geometry} = JSON.parse(event1.place);
      const eventLat = geometry.location.lat;
      const eventLon = geometry.location.lng;
      const mapId = 'mapId';

      loadMap(event1.place, mapId);

      expect(L.marker).toBeCalled();
      expect(L.marker).toBeCalledWith([eventLat, eventLon]);
    });
  });
});
