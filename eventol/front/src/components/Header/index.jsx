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
    handlerOnChangeLanguage: PropTypes.func.isRequired,
    isMobile: PropTypes.bool.isRequired,
    languages: PropTypes.arrayOf(
      PropTypes.shape({
        code: PropTypes.string,
        name: PropTypes.string,
      })
    ),
    logoHeader: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  };

  static defaultProps = {
    languages: [],
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

  wideRender = () => {
    const {logoHeader, languages, handlerOnChangeLanguage} = this.props;
    return (
      <header className="header">
        <div className="nav-wide">
          <Logo logoHeader={logoHeader} />
          <Navigation
            handlerOnChangeLanguage={handlerOnChangeLanguage}
            languages={languages}
          />
          {this.showUserIndicator()}
        </div>
      </header>
    );
  };

  render() {
    const {
      isMobile,
      logoHeader,
      languages,
      handlerOnChangeLanguage,
    } = this.props;
    if (!isMobile) return this.wideRender();
    return (
      <header className="header">
        <div className="nav-narrow">
          <Logo logoHeader={logoHeader} />
          <div className="nav-right">
            <button
              onClick={this.handleToggle}
              onKeyPress={this.handleToggle}
              type="button"
            >
              <i className="fa fa-bars fa-2x" />
            </button>
            <div className="narrow-links">
              <Navigation
                handlerOnChangeLanguage={handlerOnChangeLanguage}
                languages={languages}
              />
              {this.showUserIndicator()}
            </div>
          </div>
        </div>
      </header>
    );
  }
}
