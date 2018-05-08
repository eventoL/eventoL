import React from 'react'
import PropTypes from 'prop-types'

const PrevArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-prev fa fa-chevron-left'
    style={{...style, display: 'block', color: 'black'}}
    onClick={onClick} />
);

PrevArrow.propTypes = {
  onClick: PropTypes.func,
  style: PropTypes.object
};

export default PrevArrow;
