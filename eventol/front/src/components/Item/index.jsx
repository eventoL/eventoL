import _ from 'lodash';
import React from 'react';
import PropTypes from 'prop-types';

import ItemMap from '../ItemMap';
import {getTagUrl, goToUrl} from '../../utils/urls';

import './index.scss';

export default class Item extends React.PureComponent {
  static propTypes = {
    data: PropTypes.shape({
      attendees: PropTypes.number,
      backdrop: PropTypes.string,
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
      attendees: null,
      backdrop: null,
      tags: [],
      url: null,
    },
  };

  getTagLink = ({name, slug}) => (
    <a key={name.toLocaleLowerCase()} href={`${getTagUrl(slug)}`}>
      {name}
    </a>
  );

  handleOnClick = () => {
    const {
      data: {url},
    } = this.props;
    if (url) {
      goToUrl(url);
    }
  };

  render() {
    const {
      data: {title, attendees, overview, backdrop, eventSlug, place, url, tags},
      sliderId,
    } = this.props;
    if (!backdrop)
      return (
        <ItemMap
          attendees={attendees}
          eventSlug={eventSlug}
          overview={overview}
          place={place}
          sliderId={sliderId}
          title={title}
          url={url}
        />
      );
    return (
      <div className="item" style={{backgroundImage: `url(${backdrop})`}}>
        <div
          onClick={this.handleOnClick}
          onKeyPress={this.handleOnClick}
          role="button"
          tabIndex="0"
        >
          <div className="overlay">
            <div className="title">{title}</div>
            {!_.isNull(attendees) && !_.isUndefined(attendees) && (
              <div className="rating">
                {`${gettext('Attendees')}: ${attendees}`}
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
      </div>
    );
  }
}
