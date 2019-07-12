import React from 'react';
import PropTypes from 'prop-types';
import ItemMap from '../ItemMap';

import {getTagUrl, goToUrl} from '../../utils/urls';

import './index.scss';

export default class Item extends React.PureComponent {
  static propTypes = {
    attendees: PropTypes.number,
    backdrop: PropTypes.string,
    overview: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    url: PropTypes.string,
  };

  static defaultProps = {
    attendees: null,
    backdrop: null,
    url: null,
  };

  getTagLink = ({name, slug}) => (
    <a key={name.toLocaleLowerCase()} href={`${getTagUrl(slug)}`}>
      {name}
    </a>
  );

  handleOnClick = () => {
    const {url} = this.props;
    goToUrl(url);
  };

  render() {
    const {title, attendees, overview, backdrop, tags} = this.props;
    if (!backdrop) return <ItemMap {...this.props} />;
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
            {attendees !== null && (
              <div className="rating">
                {`${gettext('Attendees')}: ${attendees}`}
              </div>
            )}
            {tags !== undefined && (
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
