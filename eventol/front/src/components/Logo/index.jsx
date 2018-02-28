import React from 'react'
import eventolLogo from '../../assets/imgs/eventol-white.png'
import './index.scss';


const Logo = () => (
	<div id="logo" className="Logo">
		<a href='#' style={{textDecoration: 'none'}}>
	  	<img src={eventolLogo} />
		</a>
  </div>
);

export default Logo;
