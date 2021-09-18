import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Hero from '../../components/Hero';
import Header from '../../components/Header';
import {mapSizesToProps} from '../../utils/dom';
import {
  BACKGROUND_DEFAULT,
  LOGO_HEADER_DEFAULT,
  LOGO_LANDING_DEFAULT,
} from '../../utils/constants';

import './index.scss';

class InstanceDetails extends React.PureComponent {
  static propTypes = {
    background: PropTypes.string,
    events: PropTypes.number.isRequired,
    handleOnChangeLanguage: PropTypes.func,
    isMobile: PropTypes.bool.isRequired,
    languages: PropTypes.arrayOf(
      PropTypes.shape({
        code: PropTypes.string,
        name: PropTypes.string,
      })
    ),
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
    users: PropTypes.number.isRequired,
    versions: PropTypes.shape({
      commit: PropTypes.string.isRequired,
      django: PropTypes.string.isRequired,
      python: PropTypes.string.isRequired,
      tag: PropTypes.string.isRequired,
    }).isRequired,
  };

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    handleOnChangeLanguage: null,
    languages: [],
    logoHeader: LOGO_HEADER_DEFAULT,
    logoLanding: LOGO_LANDING_DEFAULT,
    user: null,
  };

  handlerOnChangeLanguage = languageCode => {
    const {handleOnChangeLanguage} = this.props;
    if (handleOnChangeLanguage) {
      handleOnChangeLanguage(languageCode);
    }
  };

  render() {
    const {
      background,
      isMobile,
      languages,
      logoHeader,
      logoLanding,
      user,
      users,
      events,
      versions,
    } = this.props;
    return (
      <div>
        <Header
          handlerOnChangeLanguage={this.handlerOnChangeLanguage}
          isMobile={isMobile}
          languages={languages}
          logoHeader={logoHeader}
          user={user}
        />
        <Hero
          background={background}
          isLogged={false}
          logoLanding={logoLanding}
          message={`EventoL ${versions.tag}`}
        >
          <h6>
            {`Users: ${users}`}
            <br />
            {`Events: ${events}`}
            <br />
            {`Django: ${versions.django}`}
            <br />
            {`Python: ${versions.python}`}
            <br />
            {`Commit: ${versions.commit}`}
          </h6>
        </Hero>
      </div>
    );
  }
}

export default withSizes(mapSizesToProps)(InstanceDetails);
