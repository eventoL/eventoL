import React from 'react'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = ({user}) => (
  <header className='Header'>
    <HeaderWide user={user}/>
    <HeaderNarrow user={user}/>
  </header>
);

export default Header;
