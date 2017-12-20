import React from 'react';
import './index.css';


export default class Hero extends React.Component {
  render = () => (
    <div id="hero" className="Hero" style={{backgroundImage: 'url(https://github.com/eventoL/eventoL/blob/master/docs/assets/background.png?raw=true)'}}>
      <div className="content">
        <p>
          <img className="logo" src="http://eventol.github.io/eventoL/assets/logo.png" alt="narcos background" />
        </p>
        <h2>Event Management Software</h2>
        {this.props.children}
      </div>
      <div className="overlay"></div>
    </div>
  );
};
