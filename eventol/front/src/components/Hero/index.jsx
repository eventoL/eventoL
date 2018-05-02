import React from 'react';
import PropTypes from 'prop-types'

import './index.scss';

export default class Hero extends React.Component {
  propTypes = {
    slug: PropTypes.string,
    children: PropTypes.element
  };

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

  render(){
    const {slug, children} = this.props;
    return (
      <div id="hero" className="Hero" style={{backgroundImage: 'url(/static/manager/img/background.png)'}}>
        <div className="content">
          <p>
            <img className="logo" src="/static/manager/img/logo.png" alt="eventol logo" />
          </p>
          { slug && (
            <h2>{`${gettext('You are seeing all of')} ${this.getSlugParsed()} ${gettext('events')}`}<br />
            {`${gettext('Please, select one to continue')}`}</h2>
        )}
          { !slug && <h2>{gettext('Search your event')}</h2> }
          {children}
        </div>
        <div className="overlay" />
      </div>
    );
  }

}
