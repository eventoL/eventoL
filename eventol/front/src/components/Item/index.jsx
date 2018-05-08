import React from 'react'
import PropTypes from 'prop-types'
import ItemMap from '../ItemMap'

import './index.scss'


export default class Item extends React.Component {
  static propTypes = {
    url: PropTypes.string,
    title: PropTypes.string,
    backdrop: PropTypes.string,
    overview: PropTypes.string,
    attendees: PropTypes.number
  };

  render(){
    const {title, url, attendees, overview, backdrop} = this.props;
    if (!backdrop) {
      return <ItemMap {...this.props} />;
    }
    return (
      <div className="Item" style={{backgroundImage: 'url(' + backdrop + ')'}} >
        <a href={url}>
          <div className="overlay">
            <div className="title">{title}</div>
            { attendees !== undefined && (<div className="rating">{gettext('Attendees')}: {attendees}</div>)}
            <div className="plot">{overview}</div>
          </div>
        </a>
      </div>
    );
  }

}
