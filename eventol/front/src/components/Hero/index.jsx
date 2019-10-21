import React from 'react';
import PropTypes from 'prop-types';

import {CREATE_EVENT} from '../../utils/urls';
import {getSlugParsed} from '../../utils/events';
import {BACKGROUND_DEFAULT, LOGO_LANDING_DEFAULT} from '../../utils/constants';

import './index.scss';

export default class Hero extends React.PureComponent {
  static propTypes = {
    background: PropTypes.string,
    children: PropTypes.oneOfType([
      PropTypes.arrayOf(PropTypes.node),
      PropTypes.node,
    ]),
    isLogged: PropTypes.bool,
    logoLanding: PropTypes.string,
    message: PropTypes.string,
    slug: PropTypes.string,
  };

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    children: null,
    isLogged: false,
    logoLanding: LOGO_LANDING_DEFAULT,
    message: null,
    slug: null,
  };

  getMessage() {
    const {slug, message} = this.props;
    if (message) {
      return <h2>{message}</h2>;
    }
    if (slug) {
      const parsedSlug = getSlugParsed(slug);
      return (
        <h2>
          {`${gettext('You are seeing all of')} ${parsedSlug} ${gettext(
            'events'
          )}`}
          <br />
          {`${gettext('Please, select one to continue')}`}
        </h2>
      );
    }
    return <h2>{gettext('Search your event')}</h2>;
  }

  render() {
    const {children, background, logoLanding, isLogged} = this.props;
    const backgroundImage = `url(${background})`;
    return (
      <div className="hero" id="hero" style={{backgroundImage}}>
        <div className="content">
          <p>
            <img alt="logo" className="logo" src={logoLanding} />
          </p>
          {isLogged && (
            <a
              className="btn btn-raised btn-warning btn-create-event"
              href={CREATE_EVENT}
            >
              {gettext('Create event')}
            </a>
          )}
          {this.getMessage()}
          {children}
        </div>
        <div className="overlay" />
      </div>
    );
  }
}
