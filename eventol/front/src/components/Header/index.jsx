import React from 'react'
import PropTypes from 'prop-types'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = ({user}) => (
  <header className='Header'>
    <HeaderWide user={user}/>
    <HeaderNarrow user={user}/>
  </header>
);

Header.propTypes = {
  user: PropTypes.object,
};

export default Header;
