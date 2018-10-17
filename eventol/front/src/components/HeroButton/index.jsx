import React from 'react';
import PropTypes from 'prop-types';
import './index.scss';


const HeroButton = ({primary, text}) => (
  <a className='button' data-primary={primary} href='#'>
    {text}
  </a>
);

HeroButton.propTypes = {
  primary: PropTypes.string,
  text: PropTypes.string,
};

export default HeroButton;
