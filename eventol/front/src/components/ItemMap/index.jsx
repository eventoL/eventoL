import React from 'react';
import ListToggle from '../ListToggle';
import './index.scss';


export default class ItemMap extends React.Component {

  loadMap(){
    const {uid:event_uid, place} = this.props;
    const {geometry} = JSON.parse(place);
    const event_lat = geometry.location.lat;
    const event_lon = geometry.location.lng;
    const map = L.map(event_uid, {
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
    const {uid} = this.props;
    try {
      this.loadMap();
    } catch(e){}
    document.getElementById(uid).classList.remove('max-size')
  }

  render(){
    const {title, url, attendees, overview, uid} = this.props;
    return (
      <div id={uid} className="Item max-size">
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
};
