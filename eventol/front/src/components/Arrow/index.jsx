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
    style: {},
    onClick: Logger.log,
  }

  getClassNameByType(){
    const {type} = this.props;
    if (type === 'prev'){
      return 'arrow-prev fa fa-chevron-left';
    }
    if (type === 'next'){
      return 'arrow-next fa fa-chevron-right';
    }
    return '';
  }

  render(){
    const {onClick, style} = this.props;
    return (
      <div
        className={`arrow ${this.getClassNameByType()}`}
        role='button'
        tabIndex='0'
        style={{...style, display: 'block', color: 'black'}}
        onKeyPress={onClick}
        onClick={onClick}
      />
    );
  }
}
