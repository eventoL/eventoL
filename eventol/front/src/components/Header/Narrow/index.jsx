import React from 'react'
import PropTypes from 'prop-types'
import Logo from '../../../components/Logo';
import NavigationNarrow from '../../../components/Navigation/Narrow';
import UserProfileNarrow from '../../../components/UserProfile/Narrow';
import SignInNarrow from '../../../components/SignIn/Narrow';
import './index.scss';


export default class HeaderNarrow extends React.PureComponent {
  static propTypes = {
    logoHeader: PropTypes.string,
    user: PropTypes.object
  };

  handleToggle(){
    const linksEl = document.querySelector('.narrow-links');
    const display = linksEl.style.display;
    linksEl.style.display = (display === 'block') ? 'none' : 'block';
  }

  render(){
    const {user, logoHeader} = this.props;
    return (
      <div className='nav-narrow'>
        <Logo logoHeader={logoHeader} />
        <div className='nav-right'>
          <a href='#' onClick={this.handleToggle}>
            <i className='fa fa-bars fa-2x' />
          </a>
          <div className='narrow-links'>
            <NavigationNarrow />
            {user && <UserProfileNarrow user={user} />}
            {!user && <SignInNarrow />}
          </div>
        </div>
      </div>
    )
  }
}
