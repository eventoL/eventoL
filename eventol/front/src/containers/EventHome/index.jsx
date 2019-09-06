import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Hero from '../../components/Hero';
import Header from '../../components/Header';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import {
  getSearchUrl,
  getMyEventsUrl,
  getUpcomingEventsUrl,
  getFinishedEventsUrl,
} from '../../utils/urls';
import {
  MOBILE_WIDTH,
  BACKGROUND_DEFAULT,
  LOGO_HEADER_DEFAULT,
  LOGO_LANDING_DEFAULT,
} from '../../utils/constants';

import './index.scss';

class EventHome extends React.PureComponent {
  static propTypes = {
    background: PropTypes.string,
    isMobile: PropTypes.bool.isRequired,
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    tagMessage: PropTypes.string,
    tagSlug: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  };

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    logoHeader: LOGO_HEADER_DEFAULT,
    logoLanding: LOGO_LANDING_DEFAULT,
    tagMessage: null,
    tagSlug: null,
    user: null,
  };

  state = {
    searchUrl: '',
    searched: false,
  };

  handleOnEnter = searchTerm => {
    const {tagSlug} = this.props;
    if (searchTerm !== '') {
      const searchUrl = getSearchUrl(searchTerm, tagSlug);
      this.setState({searchUrl, searched: true});
    }
  };

  render() {
    const {searched, searchUrl} = this.state;
    const {
      user,
      tagSlug,
      background,
      logoHeader,
      logoLanding,
      tagMessage,
      isMobile,
    } = this.props;
    return (
      <div>
        <Header isMobile={isMobile} logoHeader={logoHeader} user={user} />
        <Hero
          background={background}
          logoLanding={logoLanding}
          message={tagMessage}
          slug={tagSlug}
        >
          <Search onEnter={this.handleOnEnter} />
        </Hero>
        {searched && (
          <TitleList
            id="search_results"
            showEmpty
            title={gettext('Search results')}
            url={searchUrl}
          />
        )}
        <TitleList
          id="my_events"
          title={gettext('My Events')}
          url={getMyEventsUrl(tagSlug)}
        />
        <TitleList
          id="next"
          title={gettext('Upcoming Events')}
          url={getUpcomingEventsUrl(tagSlug)}
        />
        <TitleList
          id="finished"
          title={gettext('Finished Events')}
          url={getFinishedEventsUrl(tagSlug)}
        />
      </div>
    );
  }
}

const mapSizesToProps = ({width}) => ({
  isMobile: width < MOBILE_WIDTH,
});

export default withSizes(mapSizesToProps)(EventHome);
