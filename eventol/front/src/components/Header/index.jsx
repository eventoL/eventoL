import React from 'react'
import PropTypes from 'prop-types'
import HeaderNarrow from './Narrow';
import HeaderWide from './Wide';
import './index.scss';

const Header = ({user, logoHeader}) => (
  <header className='header'>
    <HeaderWide logoHeader={logoHeader} user={user} />
    <HeaderNarrow logoHeader={logoHeader} user={user} />
  </header>
);

Header.propTypes = {
  logoHeader: PropTypes.string,
  user: PropTypes.object
};

export default Header;
