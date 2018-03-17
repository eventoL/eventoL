import React from 'react';
import ListToggle from '../ListToggle';
import ItemMap from '../ItemMap';
import './index.scss';


export default class Item extends React.Component {

  render(){
    const {title, url, attendees, overview, backdrop, slug} = this.props;
    if (!backdrop) {
      return <ItemMap {...this.props} />;
    }
    return (
      <div className="Item" style={{backgroundImage: 'url(' + backdrop + ')'}} >
        <a href={url}>
          <div className="overlay">
            <div className="title">{title}</div>
            <div className="rating">Asistentes: {attendees}</div>
            <div className="plot">{overview}</div>
          </div>
        </a>
      </div>
    );
  }
};
