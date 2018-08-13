import React from 'react'
import PropTypes from 'prop-types'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = ({user, logoHeader}) => (
  <header className='Header'>
    <HeaderWide user={user} logoHeader={logoHeader}/>
    <HeaderNarrow user={user} logoHeader={logoHeader}/>
  </header>
);

Header.propTypes = {
  user: PropTypes.object,
  logoHeader: PropTypes.string
};

export default Header;
