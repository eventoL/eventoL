import React from 'react';
import './index.scss';

export default class Hero extends React.Component {

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
    const {slug} = this.props;
    return (
      <div id="hero" className="Hero" style={{backgroundImage: 'url(/static/manager/img/background.png)'}}>
        <div className="content">
          <p>
            <img className="logo" src="/static/manager/img/logo.png" alt="eventol logo" />
          </p>
          { slug && (
            <h2>{`${gettext('You are seeing all of')} ${this.getSlugParsed()} ${gettext('events')}`}<br></br>
            {`${gettext('Please, select one to continue')}`}</h2>
        )}
          { !slug && <h2>{gettext('Search your event')}</h2> }
          {this.props.children}
        </div>
        <div className="overlay"></div>
      </div>
    );
  }

}
