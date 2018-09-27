import React from 'react';
import PropTypes from 'prop-types';


export default class Button extends React.Component {
  static propTypes = {
    handleOnClick: PropTypes.func.isRequired,
    label: PropTypes.string,
    name: PropTypes.string,
    type: PropTypes.string
  };

  handleClick = ({target: {id}}) => {
    const {handleOnClick} = this.props;
    handleOnClick(id);
  }

  render(){
    const {type, label, name} = this.props;
    return (
      <a className={`btn btn-raised btn-${type}`} id={name} onClick={this.handleClick}>
        <span aria-hidden='true' id={name}>
          {label}
        </span>
      </a>
    );
  }
}
