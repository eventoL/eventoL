import React from 'react'
import PropTypes from 'prop-types'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = ({user, logoHeader}) => (
    <HeaderWide user={user} logoHeader={logoHeader}/>
    <HeaderNarrow user={user} logoHeader={logoHeader}/>
  <header className='header'>
  </header>
);

Header.propTypes = {
  user: PropTypes.object,
  logoHeader: PropTypes.string
};

export default Header;
