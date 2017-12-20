import React from 'react'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = () => (
  <header className='Header'>
    <HeaderWide />
    <HeaderNarrow />
  </header>
);

export default Header;
