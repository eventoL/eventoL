import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Hero from '../../components/Hero';
import Header from '../../components/Header';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import {
  MOBILE_WIDTH,
  BACKGROUND_DEFAULT,
  LOGO_HEADER_DEFAULT,
  LOGO_LANDING_DEFAULT,
} from '../../utils/constants';
import {
  getSearchUrl,
  getMyEventsUrl,
  getUpcomingEventsUrl,
  getFinishedEventsUrl,
  getEventsWithConfirmedScheduleUrl,
  getFeaturedEventsUrl,
  getRecentEventsUrl,
} from '../../utils/urls';

import './index.scss';

class Home extends React.PureComponent {
  static propTypes = {
    background: PropTypes.string,
    eventolMessage: PropTypes.string,
    isMobile: PropTypes.bool.isRequired,
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  };

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    eventolMessage: null,
    logoHeader: LOGO_HEADER_DEFAULT,
    logoLanding: LOGO_LANDING_DEFAULT,
    user: null,
  };

  state = {
    searchUrl: '',
    searched: false,
  };

  handleOnEnter = searchTerm => {
    if (searchTerm !== '') {
      const searchUrl = getSearchUrl(searchTerm);
      this.setState({searchUrl, searched: true});
    }
  };

  render() {
    const {searched, searchUrl} = this.state;
    const {
      user,
      eventolMessage,
      background,
      logoHeader,
      logoLanding,
      isMobile,
    } = this.props;
    return (
      <div>
        <Header isMobile={isMobile} logoHeader={logoHeader} user={user} />
        <Hero
          background={background}
          logoLanding={logoLanding}
          message={eventolMessage}
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
          url={getMyEventsUrl()}
        />
        <TitleList
          id="recent"
          title={gettext('Recent Events')}
          url={getRecentEventsUrl()}
        />
        <TitleList
          id="featured"
          title={gettext('Featured Events')}
          url={getFeaturedEventsUrl()}
        />
        <TitleList
          id="next"
          title={gettext('Upcoming Events')}
          url={getUpcomingEventsUrl()}
        />
        <TitleList
          id="schedule_confirmed"
          title={gettext('Events with Confirmed Schedule')}
          url={getEventsWithConfirmedScheduleUrl()}
        />
        <TitleList
          id="finished"
          title={gettext('Finished Events')}
          url={getFinishedEventsUrl()}
        />
      </div>
    );
  }
}

const mapSizesToProps = ({width}) => ({
  isMobile: width < MOBILE_WIDTH,
});

export default withSizes(mapSizesToProps)(Home);
