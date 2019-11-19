import React from 'react';
import PropTypes from 'prop-types';

import {INDEX_URL} from '../../utils/urls';
import {LOGO_HEADER_DEFAULT} from '../../utils/constants';

import './index.scss';


const Logo = ({logoHeader}) => (
  <div className='logo-component' id='logo'>
    <a href={INDEX_URL}>
      <img alt='header logo' src={logoHeader} />
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
