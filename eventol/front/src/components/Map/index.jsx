import React, {useEffect} from 'react';
import PropTypes from 'prop-types';

import Logger from '../../utils/logger';
import {getMapId, loadMap} from '../../utils/map';

import './index.scss';

const Map = props => {
  const {children, place, eventSlug, sliderId} = props;
  const mapId = getMapId(eventSlug, sliderId);

  useEffect(() => {
    try {
      loadMap(place, mapId);
    } catch (e) {
      Logger.error(e);
    }
    document.getElementById(mapId).classList.remove('max-size');
  }, [mapId, place]);

  return (
    <div className="item max-size" id={mapId}>
      {children}
    </div>
  );
};

Map.propTypes = {
  children: PropTypes.node.isRequired,
  eventSlug: PropTypes.string.isRequired,
  place: PropTypes.string.isRequired,
  sliderId: PropTypes.string.isRequired,
};

export default Map;
