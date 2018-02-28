import React from 'react'
import Logo from '../../../components/Logo';
import Navigation from '../../../components/Navigation';
import UserProfile from '../../../components/UserProfile';
import './index.scss';


const HeaderWide = ({user}) => (
  <div className="navWide">
    <Logo />
    <Navigation />
    <UserProfile user={user}/>
  </div>
);

export default HeaderWide;
