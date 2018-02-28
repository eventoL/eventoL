import React from 'react';
import ListToggle from '../ListToggle';
import './index.scss';


export default class ItemMap extends React.Component {

  loadMap(){
    const {slug:event_name, place} = this.props;
    const {geometry} = JSON.parse(place);
    const event_lat = geometry.location.lat;
    const event_lon = geometry.location.lng;
    const map = L.map(event_name, {
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
    const {slug} = this.props;
    try {
      this.loadMap();
    } catch(e){}
    document.getElementById(slug).classList.remove('max-size')
  }

  render(){
    const {title, url, attendees, overview, slug} = this.props;
    return (
      <div id={slug} className="Item max-size">
        <a href={url} style={{textDecoration: 'none'}}>
          <div className="overlay">
            <div className="title">{title}</div>
            <div className="rating">Asistentes: {attendees}</div>
            <div className="plot">{overview}</div>
          </div>
        </a>
      </div>
    )
  }
};
