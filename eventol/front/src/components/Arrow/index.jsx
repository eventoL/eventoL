import React from 'react';
import PropTypes from 'prop-types';

import Logger from '../../utils/logger';

export default class Arrow extends React.PureComponent {
  static propTypes = {
    onClick: PropTypes.func,
    style: PropTypes.shape({}),
    type: PropTypes.oneOf(['prev', 'next']).isRequired,
  };

  static defaultProps = {
    onClick: Logger.log,
    style: {},
  };

  getClassNameByType() {
    const {type} = this.props;
    if (type === 'prev') {
      return 'arrow-prev fa fa-chevron-left';
    }
    if (type === 'next') {
      return 'arrow-next fa fa-chevron-right';
    }
    return '';
  }

  handleOnClick = event => {
    event.preventDefault();
    event.stopPropagation();
    const {onClick} = this.props;
    onClick();
  };

  render() {
    const {style} = this.props;
    return (
      <div
        className={`arrow ${this.getClassNameByType()}`}
        onClick={this.handleOnClick}
        onKeyPress={this.handleOnClick}
        role="button"
        style={{...style, display: 'block', color: 'black'}}
        tabIndex="0"
      />
    );
  }
}
