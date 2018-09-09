import React from 'react';
import PropTypes from 'prop-types'
import './index.scss';


export default class ItemMap extends React.PureComponent {
  static propTypes = {
    attendees: PropTypes.number,
    event_slug: PropTypes.string,
    overview: PropTypes.string,
    place: PropTypes.string,
    sliderId: PropTypes.string,
    title: PropTypes.string,
    url: PropTypes.string
  }

  componentDidMount(){
    const event_slug = this.getMapId();
    try {
      this.loadMap();
    } catch(e){
      console.error(e);
    }
    document.getElementById(event_slug).classList.remove('max-size');
  }

  getMapId(){
    const {event_slug, sliderId} = this.props;
    return `${sliderId}${event_slug}`;
  }

  loadMap(){
    const {place} = this.props;
    const {geometry} = JSON.parse(place);
    const event_lat = geometry.location.lat;
    const event_lon = geometry.location.lng;
    const mapId = this.getMapId();
    // TODO: move to constant
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

  render(){
    const {title, url, attendees, overview} = this.props;
    const mapId = this.getMapId();
    return (
      <div className='item max-size' id={mapId}>
        <a href={url}>
          <div className='overlay'>
            <div className='title'>{title}</div>
            <div className='rating'>{gettext('Attendees')}: {attendees}</div>
            <div className='plot'>{overview}</div>
          </div>
        </a>
      </div>
    )
  }
}
