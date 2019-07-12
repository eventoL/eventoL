import React from 'react';
import PropTypes from 'prop-types';

import Logo from '../Logo';
import Navigation from '../Navigation';
import UserProfile from '../UserProfile';
import SignIn from '../SignIn';

import './index.scss';
import {LOGO_HEADER_DEFAULT} from '../../utils/constants';

export default class Header extends React.PureComponent {
  static propTypes = {
    isMobile: PropTypes.bool.isRequired,
    logoHeader: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  };

  static defaultProps = {
    logoHeader: LOGO_HEADER_DEFAULT,
    user: null,
  };

  handleToggle = event => {
    event.preventDefault();
    event.stopPropagation();
    const linksEl = document.querySelector('.narrow-links');
    const {
      style: {display},
    } = linksEl;
    linksEl.style.display = display === 'block' ? 'none' : 'block';
  };

  showUserIndicator = () => {
    const {user} = this.props;
    if (user) return <UserProfile user={user} />;
    return <SignIn />;
  };

  mobileRender = () => {
    const {logoHeader} = this.props;
    return (
      <header className="header">
        <div className="nav-wide">
          <Logo logoHeader={logoHeader} />
          <Navigation />
          {this.showUserIndicator()}
        </div>
      </header>
    );
  };

  render() {
    const {isMobile, logoHeader} = this.props;
    if (!isMobile) return this.mobileRender();
    return (
      <header className="header">
        <div className="nav-narrow">
          <Logo logoHeader={logoHeader} />
          <div className="nav-right">
            <a href="#" onClick={this.handleToggle}>
              <i className="fa fa-bars fa-2x" />
            </a>
            <div className="narrow-links">
              <Navigation />
              {this.showUserIndicator()}
            </div>
          </div>
        </div>
      </header>
    );
  }
}
