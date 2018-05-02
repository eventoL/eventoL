import React from 'react';
import PropTypes from 'prop-types'
import './index.scss';


export default class ItemMap extends React.Component {
  propTypes = {
    place: PropTypes.string,
    title: PropTypes.string,
    url: PropTypes.string,
    attendees: PropTypes.string,
    overview: PropTypes.string,
    uid: PropTypes.string,
    sliderId: PropTypes.string
  };

  getMapId(){
    const {uid, sliderId} = this.props;
    return `${sliderId}${uid}`;
  }

  loadMap(){
    const {place} = this.props;
    const {geometry} = JSON.parse(place);
    const event_lat = geometry.location.lat;
    const event_lon = geometry.location.lng;
    const mapId = this.getMapId();
    const map = L.map(mapId, {
        scrollWheelZoom: false,
        zoomControl    : false,
        dragging       : false,
        keyboard       : false,
        doubleClickZoom: false,
        touchZoom      : false,
        boxZoom        : false,
        minZoom: 11,
        maxZoom: 11
    }).setView([event_lat, event_lon], 5);
    L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
        attribution: ''
    }).addTo(map);
    map.attributionControl.setPrefix('');
    L.marker([event_lat, event_lon]).addTo(map);
  }

  componentDidMount(){
    const uid = this.getMapId();
    try {
      this.loadMap();
    } catch(e){}
    document.getElementById(uid).classList.remove('max-size')
  }

  render(){
    const {title, url, attendees, overview, uid, sliderId} = this.props;
    const mapId = this.getMapId();
    return (
      <div id={mapId} className="Item max-size">
        <a href={url}>
          <div className="overlay">
            <div className="title">{title}</div>
            <div className="rating">{gettext('Attendees')}: {attendees}</div>
            <div className="plot">{overview}</div>
          </div>
        </a>
      </div>
    )
  }
}
