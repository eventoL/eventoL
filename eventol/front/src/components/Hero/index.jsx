import React from 'react';
import PropTypes from 'prop-types'

import './index.scss';

export default class Hero extends React.Component {
  static propTypes = {
    slug: PropTypes.string,
    message: PropTypes.string,
    background: PropTypes.string,
    logoLanding: PropTypes.string,
    children: PropTypes.oneOfType([
      PropTypes.array,
      PropTypes.object,
      PropTypes.element
    ])
  }

  static defaultProps = {
    background: '/static/manager/img/background.png',
    logoLanding: '/static/manager/img/logo.png'
  }

  getSlugParsed(){
    const {slug} = this.props;
    return slug
      .toLowerCase()
      .split('-')
      .join(' ')
      .split('_')
      .join(' ')
      .split(' ')
      .map(word => (word) ? word.replace(word[0], word[0].toUpperCase()) : '')
      .join(' ');
  }

  getMessage(){
    const {slug, message} = this.props;
    if (message) return <h2>{message}</h2>;
    if (slug) return (
      <h2>{`${gettext('You are seeing all of')} ${this.getSlugParsed()} ${gettext('events')}`}<br />
      {`${gettext('Please, select one to continue')}`}</h2>
    );
    return <h2>{gettext('Search your event')}</h2>;
  }

  render(){
    const {children, background, logoLanding} = this.props;
    const backgroundImage = `url(${background})`;
    return (
        <div className="content">
      <div className='hero' id='hero' style={{backgroundImage}}>
          <p>
            <img className="logo" src={logoLanding} alt="logo" />
          </p>
          { this.getMessage() }
          {children}
        </div>
        <div className="overlay" />
      </div>
    );
  }

}
