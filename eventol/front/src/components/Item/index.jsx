import React from 'react';
import ListToggle from '../ListToggle';
import './index.css';


export default class Item extends React.Component {
  render(){
    return (
      <div className="Item" style={{backgroundImage: 'url(' + this.props.backdrop + ')'}} >
        <div className="overlay">
          <div className="title">{this.props.title}</div>
          <div className="rating">Asistentes: {this.props.attendees}</div>
          <div className="plot">{this.props.overview}</div>
          <ListToggle />
        </div>
      </div>
    );
  }
};
