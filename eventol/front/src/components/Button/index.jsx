import React from 'react';


export default class Button extends React.Component {
  handleClick = ({target: {id}}) => {
    event.stopPropagation();
    event.preventDefault();
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
