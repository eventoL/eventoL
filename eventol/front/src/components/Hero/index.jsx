import React from 'react';
import PropTypes from 'prop-types';

import './index.scss';

export default class Hero extends React.Component {
  static propTypes = {
    background: PropTypes.string,
    children: PropTypes.oneOfType([
      PropTypes.array,
      PropTypes.object,
      PropTypes.element
      // TODO: search children proptypes details
    ]),
    logoLanding: PropTypes.string,
    message: PropTypes.string,
    slug: PropTypes.string
  }

  static defaultProps = {
    background: '/static/manager/img/background.png', // TODO: move to constant
    logoLanding: '/static/manager/img/logo.png' // TODO: move to constant
  }

  getSlugParsed(){ // TODO: move to utils
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
    if (message) {
      return <h2>{message}</h2>;
    }
    if (slug) {
      return (
        <h2>
          {`${gettext('You are seeing all of')} ${this.getSlugParsed()} ${gettext('events')}`}
          <br />
          {`${gettext('Please, select one to continue')}`}
        </h2>
      );
    }
    return <h2>{gettext('Search your event')}</h2>;
  }

  render(){
    const {children, background, logoLanding} = this.props;
    const backgroundImage = `url(${background})`;
    return (
      <div className='hero' id='hero' style={{backgroundImage}}>
        <div className='content'>
          <p><img alt='logo' className='logo' src={logoLanding} /></p>
          {this.getMessage()}
          {children}
        </div>
        <div className='overlay' />
      </div>
    );
  }
}
