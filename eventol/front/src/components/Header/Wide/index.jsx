import React from 'react'
import Logo from '../../../components/Logo';
import Navigation from '../../../components/Navigation';
import UserProfile from '../../../components/UserProfile';
import './index.scss';


const HeaderWide = () => (
  <div className="navWide">
    <Logo />
    <Navigation />
    <UserProfile />
  </div>
);

export default HeaderWide;
