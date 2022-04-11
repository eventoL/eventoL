import 'leaflet/dist/leaflet.css';

import 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const icons = {
  iconAnchor: [12, 25],
  iconSize: [25, 41],
  iconUrl: icon,
  shadowAnchor: [20, 41],
  shadowSize: [41, 41],
  shadowUrl: iconShadow,
};
L.Marker.prototype.options.icon = L.icon(icons);

const addCard = (cardId, lat, lng, dirflg) => {
  $(`#${cardId}`).attr(
    'href',
    `https://maps.google.com/?saddr=Current+Location&daddr=${lat},${lng}&dirflg=${dirflg}`
  );
};

const loadMap = place => {
  const {
    name,
    adr_address: address,
    geometry: {
      location: {lat, lng},
    },
  } = place;
  const map = L.map('map', {
    scrollWheelZoom: false,
    touchZoom: false,
  }).setView([lat, lng], 14);

  L.tileLayer(
    'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png',
    {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>',
    }
  ).addTo(map);
  map.attributionControl.setPrefix('');

  const marker = L.marker([lat, lng]).addTo(map);

  const multiplyPointBy = (zoomLevel, point) => {
    const width = point[0];
    const height = point[1];
    const factor = (18 - zoomLevel) / 30 + 1;
    const newPoint = L.point(width / factor, height / factor);

    return newPoint;
  };

  const scaleIcon = zoomLevel => {
    const newIcon = L.icon({
      ...icons,
      iconAnchor: multiplyPointBy(zoomLevel, icons.iconAnchor),
      iconSize: multiplyPointBy(zoomLevel, icons.iconSize),
      shadowAnchor: multiplyPointBy(zoomLevel, icons.shadowAnchor),
      shadowSize: multiplyPointBy(zoomLevel, icons.shadowSize),
    });

    return newIcon;
  };

  const resizeIcon = () => {
    const zoomLevel = map.getZoom();
    const markerIcon = scaleIcon(zoomLevel);
    marker.setIcon(markerIcon);
    marker.setLatLng([lat, lng]);
  };

  map.whenReady(resizeIcon);
  map.on('zoomend', resizeIcon);

  $('#place_name').text(name);
  $('#address1').html(address);

  addCard('directions-car', lat, lng, 'd');
  addCard('directions-walk', lat, lng, 'w');
  addCard('directions-bus', lat, lng, 'r');
  addCard('directions-bike', lat, lng, 'b');
};

if (!window.libs) {
  window.libs = {};
}
window.libs.map = loadMap;
