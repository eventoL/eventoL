import React from 'react';
import PropTypes from 'prop-types';
import Logo from '../../../components/Logo';
import Navigation from '../../../components/Navigation';
import UserProfile from '../../../components/UserProfile';
import SignIn from '../../../components/SignIn';

import './index.scss';


const HeaderWide = ({user, logoHeader}) => (
  <div className='nav-wide'>
    <Logo logoHeader={logoHeader} />
    <Navigation />
    {user && <UserProfile user={user} />}
    {/*TODO: move user condition to function */}
    {!user && <SignIn />}
  </div>
);

HeaderWide.propTypes = {
  logoHeader: PropTypes.string,
  user: PropTypes.object
};

export default HeaderWide;
