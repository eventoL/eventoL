import React from 'react';
import PropTypes from 'prop-types'
import './index.scss';


export default class HeroButton extends React.Component {
  propTypes = {
    primary: PropTypes.string,
    text: PropTypes.string
  };

  render(){
    const {primary, text} = this.props;
    return (
      <a href="#" className="Button" data-primary={primary}>{text}</a>
    );
  }
}
