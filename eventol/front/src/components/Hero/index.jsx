import React from 'react';
import './index.scss';


export default class Hero extends React.Component {
  render = () => (
    <div id="hero" className="Hero" style={{backgroundImage: 'url(/static/manager/img/background.png)'}}>
      <div className="content">
        <p>
          <img className="logo" src="/static/manager/img/logo.png" alt="eventol logo" />
        </p>
        <h2>Event Management Software</h2>
        {this.props.children}
      </div>
      <div className="overlay"></div>
    </div>
  );
};
