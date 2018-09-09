import React from 'react'
import PropTypes from 'prop-types'
import Logo from '../../../components/Logo'
import Navigation from '../../../components/Navigation'
import UserProfile from '../../../components/UserProfile'
import SignIn from '../../../components/SignIn'

import './index.scss'


const HeaderWide = ({user, logoHeader}) => (
    <Logo logoHeader={logoHeader}/>
  <div className='nav-wide'>
    <Navigation />
    {user && <UserProfile user={user}/>}
    {!user && <SignIn/>}
  </div>
);

HeaderWide.propTypes = {
  user: PropTypes.object,
  logoHeader: PropTypes.string
};

export default HeaderWide;
