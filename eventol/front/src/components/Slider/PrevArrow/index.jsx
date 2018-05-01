import React from 'react'

const PrevArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-prev fa fa-chevron-left'
    style={{...style, display: 'block', color: 'black'}}
    onClick={onClick} />
);

export default PrevArrow;
