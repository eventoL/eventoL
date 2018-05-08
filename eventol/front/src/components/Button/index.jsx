import React from 'react';
import PropTypes from 'prop-types'


export default class Button extends React.Component {
  static propTypes = {
    name: PropTypes.string,
    label: PropTypes.string,
    type: PropTypes.string,
    handleOnClick: PropTypes.func
  };

  handleClick = ({target: {id}}) => {
    const {handleOnClick} = this.props;
    if (handleOnClick) handleOnClick(id);
  }

  render(){
    const {type, label, name} = this.props;
    return (
      <a id={name} onClick={this.handleClick} className={`btn btn-raised btn-${type}`}>
        <span id={name} aria-hidden="true">{label}</span>
      </a>
    );
  }
}
