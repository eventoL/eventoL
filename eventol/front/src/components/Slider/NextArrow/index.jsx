import React from 'react';
import PropTypes from 'prop-types';


// TODO: merge with prev arrow
const NextArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-next fa fa-chevron-right'
    onClick={onClick}
    style={{...style, display: 'block', color: 'black'}}
  />
);

NextArrow.propTypes = {
  onClick: PropTypes.func,
  style: PropTypes.object,
};

export default NextArrow;
