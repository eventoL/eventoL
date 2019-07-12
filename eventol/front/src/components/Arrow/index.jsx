import React from 'react';
import PropTypes from 'prop-types';

import Logger from '../../utils/logger';

export default class Arrow extends React.PureComponent {
  static propTypes = {
    handleOnClick: PropTypes.func,
    style: PropTypes.shape({}),
    type: PropTypes.oneOf(['prev', 'next']).isRequired,
  };

  static defaultProps = {
    handleOnClick: Logger.log,
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

  render() {
    const {handleOnClick, style} = this.props;
    return (
      <div
        className={`arrow ${this.getClassNameByType()}`}
        onClick={handleOnClick}
        onKeyPress={handleOnClick}
        role="button"
        style={{...style, display: 'block', color: 'black'}}
        tabIndex="0"
      />
    );
  }
}
