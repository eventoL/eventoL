import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'


const Logo = ({logoHeader}) => (
	<div id="logo" className="Logo">
		<a href='/'>
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
