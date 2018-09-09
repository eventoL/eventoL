import React from 'react'
import PropTypes from 'prop-types'
import ItemMap from '../ItemMap'

import {getTagUrl} from '../../utils/urls'

import './index.scss'


const Item = props => {
  const {title, url, attendees, overview, backdrop, tags} = props;
  if (!backdrop) return <ItemMap {...props} />;
  return (
    <div className='item' style={{backgroundImage: 'url(' + backdrop + ')'}} >
      <a href={url}>
        <div className='overlay'>
          <div className='title'>
            {title}
          </div>
          { attendees !== undefined && (
            <div className='rating'>
              {gettext('Attendees')}: {attendees}
            </div>
          )}
          { tags !== undefined && (
            <div className='rating tags'>
              {gettext('Tags')}: {tags.map(({name, slug}, index) => <a key={index} href={`${getTagUrl(slug)}`}>{name}</a>)}
            </div>
          )}
          <div className='plot'>
            {overview}
          </div>
        </div>
      </a>
    </div>
  );
};

Item.propTypes = {
  attendees: PropTypes.number,
  backdrop: PropTypes.string,
  overview: PropTypes.string,
  title: PropTypes.string,
  url: PropTypes.string
};

export default Item;
