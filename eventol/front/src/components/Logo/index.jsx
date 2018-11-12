import React from 'react';
import PropTypes from 'prop-types';

import {LOGO_HEADER_DEFAULT} from '../../utils/constants';

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
  logoHeader: LOGO_HEADER_DEFAULT,
};

export default Logo;
