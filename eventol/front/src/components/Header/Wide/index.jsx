import React from 'react'
import Logo from '../../../components/Logo';
import Navigation from '../../../components/Navigation';
import UserProfile from '../../../components/UserProfile';
import SignIn from '../../../components/SignIn';
import './index.scss';


const HeaderWide = ({user}) => (
  <div className="navWide">
    <Logo />
    <Navigation />
    {user && <UserProfile user={user}/>}
    {!user && <SignIn/>}
  </div>
);

export default HeaderWide;
