import React from 'react'
import PropTypes from 'prop-types'
import ReactSlickSlider from 'react-slick'

import NextArrow from './NextArrow';
import PrevArrow from './PrevArrow';
import {SLIDER_BASE_SETTINGS} from '../../utils/constants';

import './index.css';


const Slider = ({children:items}) => {
  const settings = {
    ...SLIDER_BASE_SETTINGS,
    prevArrow: <PrevArrow />,
    nextArrow: <NextArrow />
  }
  return (
    <ReactSlickSlider className='container' {...settings}>
      {items}
    </ReactSlickSlider>
  );
};

Slider.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.array,
    PropTypes.object,
    PropTypes.element
  ])
};

export default Slider;
