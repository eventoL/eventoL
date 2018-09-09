import React from 'react'
import PropTypes from 'prop-types'
import Logo from '../../../components/Logo';
import NavigationNarrow from '../../../components/Navigation/Narrow';
import UserProfileNarrow from '../../../components/UserProfile/Narrow';
import SignInNarrow from '../../../components/SignIn/Narrow';
import './index.scss';


export default class HeaderNarrow extends React.Component {

  static propTypes = {
    user: PropTypes.object,
    logoHeader: PropTypes.string
  };

  toggle(){
		const linksEl = document.querySelector('.narrowLinks');
    const display = linksEl.style.display;
    linksEl.style.display = (display === 'block') ? 'none' : 'block';
	}

  render(){
    const {user, logoHeader} = this.props;
    return (
        <Logo logoHeader={logoHeader}/>
          <a href="#" onClick={this.toggle}><i className="fa fa-bars fa-2x" /></a>
      <div className='nav-narrow'>
        <div className='nav-right'>
          <div className='narrow-links'>
            <NavigationNarrow />
            {user && <UserProfileNarrow user={user}/>}
            {!user && <SignInNarrow/>}
          </div>
        </div>
      </div>
    )
  }
}
