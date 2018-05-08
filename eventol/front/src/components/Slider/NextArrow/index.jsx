import React from 'react'
import PropTypes from 'prop-types'

const NextArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-next fa fa-chevron-right'
    style={{...style, display: 'block', color: 'black'}}
    onClick={onClick} />
);

NextArrow.propTypes = {
  onClick: PropTypes.func,
  style: PropTypes.object
};

export default NextArrow;
