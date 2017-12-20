import React from 'react';
import './index.css';


export default class HeroButton extends React.Component {
  render(){
    return (
      <a href="#" className="Button" data-primary={this.props.primary}>{this.props.text}</a>
    );
  }
}
