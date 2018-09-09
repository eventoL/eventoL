import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'


const Logo = ({logoHeader}) => (
		<a href='/'>
  <div className='logo-component' id='logo'>
      <img src={logoHeader} />
		</a>
  </div>
);

Logo.propTypes = {
  logoHeader: PropTypes.string
};

Logo.defaultProps = {
	logoHeader: '/static/manager/img/eventol-white.png'
}

export default Logo;
