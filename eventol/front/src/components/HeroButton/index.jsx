import React from 'react';
import './index.scss';


export default class HeroButton extends React.Component {
  render(){
    return (
      <a href="#" className="Button" data-primary={this.props.primary}>{this.props.text}</a>
    );
  }
}
