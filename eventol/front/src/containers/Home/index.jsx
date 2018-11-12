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
  getSearchUrl, getMyEventsUrl,
  getUpcommingEventsUrl,
  getFinishedEventsUrl,
  getEventsWithConfirmedScheduleUrl,
  getFeaturedEventsUrl,
  getRecentEventsUrl,
} from '../../utils/urls';

import './index.scss';


class Home extends React.Component {
  static propTypes = {
    isMobile: PropTypes.bool.isRequired,
    background: PropTypes.string,
    eventolMessage: PropTypes.string,
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  }

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    logoHeader: LOGO_HEADER_DEFAULT,
    logoLanding: LOGO_LANDING_DEFAULT,
    eventolMessage: null,
    user: null,
  }

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false,
  }

  handleOnEnter = () => {
    const {searchTerm} = this.state;
    if (searchTerm !== ''){
      const searchUrl = getSearchUrl(searchTerm);
      this.setState({searchUrl, searched: true});
    }
  }

  handleOnChange = searchTerm => this.setState({searchTerm})

  render(){
    const {searched, searchUrl} = this.state;
    const {
      user, eventolMessage, background,
      logoHeader, logoLanding, isMobile,
    } = this.props;
    return (
      <div>
        <Header logoHeader={logoHeader} user={user} isMobile={isMobile} />
        <Hero background={background} logoLanding={logoLanding} message={eventolMessage}>
          <Search onChange={this.handleOnChange} onEnter={this.handleOnEnter} />
        </Hero>
        {searched && <TitleList showEmpty id='search_results' title={gettext('Search results')} url={searchUrl} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={getMyEventsUrl()}
        />
        <TitleList
          id='recent'
          title={gettext('Recent Events')}
          url={getRecentEventsUrl()}
        />
        <TitleList
          id='featured'
          title={gettext('Featured Events')}
          url={getFeaturedEventsUrl()}
        />
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={getUpcommingEventsUrl()}
        />
        <TitleList
          id='schedule_confirmed'
          title={gettext('Events with Confirmed Schedule')}
          url={getEventsWithConfirmedScheduleUrl()}
        />
        <TitleList
          id='finished'
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
