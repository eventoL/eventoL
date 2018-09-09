import React from 'react'
import PropTypes from 'prop-types'

const PrevArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-prev fa fa-chevron-left'
    onClick={onClick}
    style={{...style, display: 'block', color: 'black'}}
  />
);

PrevArrow.propTypes = {
  onClick: PropTypes.func,
  style: PropTypes.object
};

export default PrevArrow;
