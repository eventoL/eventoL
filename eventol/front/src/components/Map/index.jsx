import React from 'react';
import PropTypes from 'prop-types';

import Logger from '../../utils/logger';
import {MAP_SETTINGS, MAP_LAYER} from '../../utils/constants';

import './index.scss';

export default class Map extends React.PureComponent {
  static propTypes = {
    children: PropTypes.element.isRequired,
    eventSlug: PropTypes.string.isRequired,
    place: PropTypes.string.isRequired,
    sliderId: PropTypes.string.isRequired,
  };

  componentDidMount() {
    const eventSlug = this.getMapId();
    try {
      this.loadMap();
    } catch (e) {
      Logger.error(e);
    }
    document.getElementById(eventSlug).classList.remove('max-size');
  }

  getMapId() {
    const {eventSlug, sliderId} = this.props;
    return `${sliderId}${eventSlug}`;
  }

  loadMap() {
    const {place} = this.props;
    const {geometry} = JSON.parse(place);
    const eventLat = geometry.location.lat;
    const eventLon = geometry.location.lng;
    const mapId = this.getMapId();
    const map = L.map(mapId, MAP_SETTINGS).setView([eventLat, eventLon], 5);
    L.tileLayer(MAP_LAYER, {attribution: ''}).addTo(map);
    map.attributionControl.setPrefix('');
    L.marker([eventLat, eventLon]).addTo(map);
  }

  render() {
    const {children} = this.props;
    const mapId = this.getMapId();
    return (
      <div className="item max-size" id={mapId}>
        {children}
      </div>
    );
  }
}
