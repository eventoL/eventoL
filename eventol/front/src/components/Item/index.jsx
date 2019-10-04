import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';

import Map from '../Map';
import {getTagUrl, goToUrl} from '../../utils/urls';

import './index.scss';

export default class Item extends React.PureComponent {
  static propTypes = {
    data: PropTypes.shape({
      attendees: PropTypes.number,
      backdrop: PropTypes.string,
      empty: PropTypes.bool,
      eventSlug: PropTypes.string.isRequired,
      overview: PropTypes.string.isRequired,
      place: PropTypes.string.isRequired,
      tags: PropTypes.arrayOf(
        PropTypes.shape({
          name: PropTypes.string.isRequired,
          slug: PropTypes.string.isRequired,
        })
      ),
      title: PropTypes.string.isRequired,
      url: PropTypes.string,
    }),
    sliderId: PropTypes.string.isRequired,
  };

  static defaultProps = {
    data: {
      backdrop: null,
      tags: [],
      empty: true,
      url: null,
    },
  };

  getTagLink = ({name, slug}) => (
    <a key={name.toLocaleLowerCase()} href={`${getTagUrl(slug)}`}>
      {name}
    </a>
  );

  handleOnClick = event => {
    event.preventDefault();
    event.stopPropagation();
    const {
      data: {url},
    } = this.props;
    if (url) {
      goToUrl(url);
    }
  };

  getItem = () => {
    const {
      data: {title, attendees, overview, tags, empty},
    } = this.props;
    return (
      <div
        onClick={this.handleOnClick}
        onKeyPress={this.handleOnClick}
        role="button"
        tabIndex="0"
      >
        <div className="overlay">
          <div className="title">{title}</div>
          {!empty && (
            <div className="rating">
              {`${gettext('Attendees')}: ${attendees || 0}`}
            </div>
          )}
          {!_.isEmpty(tags) && (
            <div className="rating tags">
              {/* eslint-disable-next-line react/jsx-one-expression-per-line */}
              {gettext('Tags')}: {tags.map(this.getTagLink)}
            </div>
          )}
          <div className="plot">{overview}</div>
        </div>
      </div>
    );
  };

  render() {
    const {
      data: {backdrop, eventSlug, place},
      sliderId,
    } = this.props;
    const item = this.getItem();
    if (!backdrop)
      return (
        <Map eventSlug={eventSlug} place={place} sliderId={sliderId}>
          {item}
        </Map>
      );
    return (
      <div className="item" style={{backgroundImage: `url(${backdrop})`}}>
        {item}
      </div>
    );
  }
}
