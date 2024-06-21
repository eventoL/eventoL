import React from 'react';
import PropTypes from 'prop-types';

export default class Button extends React.PureComponent {
  static propTypes = {
    handleOnClick: PropTypes.func.isRequired,
    label: PropTypes.string,
    name: PropTypes.string,
    type: PropTypes.oneOf([
      'default',
      'primary',
      'success',
      'info',
      'warning',
      'danger',
      'link',
    ]),
  };

  static defaultProps = {
    label: '',
    name: 'btn',
    type: 'default',
  };

  handleClick = event => {
    event.preventDefault();
    event.stopPropagation();
    const {handleOnClick} = this.props;
    handleOnClick(event.target.id);
  };

  render() {
    const {type, label, name} = this.props;
    const className = `btn btn-raised btn-${type}`;
    return (
      <button
        className={className}
        id={name}
        onClick={this.handleClick}
        type="button"
      >
        <span aria-hidden id={name}>
          {label}
        </span>
      </button>
    );
  }
}
