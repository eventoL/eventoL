import Logger from './logger';
import {MAP_SETTINGS, MAP_LAYER} from './constants';

export const getMapId = (eventSlug, sliderId) => `${sliderId}${eventSlug}`;

export const loadMap = (place, mapId) => {
  try {
    const {geometry} = JSON.parse(place);
    const eventLat = geometry.location.lat;
    const eventLon = geometry.location.lng;
    const map = L.map(mapId, MAP_SETTINGS).setView([eventLat, eventLon], 5);
    L.tileLayer(MAP_LAYER, {attribution: ''}).addTo(map);
    map.attributionControl.setPrefix('');
    L.marker([eventLat, eventLon]).addTo(map);
  } catch (e) {
    Logger.error(e);
  }
};
