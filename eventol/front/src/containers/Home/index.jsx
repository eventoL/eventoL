import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Hero from '../../components/Hero';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import {mapSizesToProps} from '../../utils/dom';
import {BACKGROUND_DEFAULT, LOGO_LANDING_DEFAULT} from '../../utils/constants';
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
    handleOnChangeLanguage: PropTypes.func,
    logoLanding: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  };

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    eventolMessage: null,
    handleOnChangeLanguage: null,
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

  handlerOnChangeLanguage = languageCode => {
    const {handleOnChangeLanguage} = this.props;
    if (handleOnChangeLanguage) {
      handleOnChangeLanguage(languageCode);
    }
  };

  render() {
    const {searched, searchUrl} = this.state;
    const {user, eventolMessage, background, logoLanding} = this.props;
    return (
      <div>
        <Hero
          background={background}
          isLogged={user !== null}
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

export default withSizes(mapSizesToProps)(Home);
