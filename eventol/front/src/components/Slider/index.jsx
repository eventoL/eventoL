import React from 'react';
import PropTypes from 'prop-types';
import ReactSlickSlider from 'react-slick';

import Arrow from '../Arrow';
import {SLIDER_BASE_SETTINGS} from '../../utils/constants';

import './index.css';


const Slider = ({children: items}) => {
  const settings = {
    ...SLIDER_BASE_SETTINGS,
    prevArrow: <Arrow type='prev' />,
    nextArrow: <Arrow type='next' />,
  };
  return (
    <ReactSlickSlider className='container' {...settings}>
      {items}
    </ReactSlickSlider>
  );
};

Slider.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
};

Slider.defaultProps = {
  children: null,
};

export default Slider;
