import React from 'react';
import PropTypes from 'prop-types';

import './index.scss';


const Logo = ({logoHeader}) => (
  <div className='logo-component' id='logo'>
    <a href='/'>
      <img src={logoHeader} />
    </a>
  </div>
);

Logo.propTypes = {
  logoHeader: PropTypes.string,
};

Logo.defaultProps = {
  logoHeader: '/static/manager/img/eventol-white.png', // TODO: move to constant
};

export default Logo;
