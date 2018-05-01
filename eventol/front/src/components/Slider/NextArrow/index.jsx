import React from 'react'

const NextArrow = ({onClick, style}) => (
  <div
    className='arrow arrow-next fa fa-chevron-right'
    style={{...style, display: 'block', color: 'black'}}
    onClick={onClick} />
);

export default NextArrow;
