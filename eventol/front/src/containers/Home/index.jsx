import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Header from '../../components/Header';
import Hero from '../../components/Hero';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import {HOME_REQUIRED_FIELDS} from '../../utils/constants';

import './index.scss';


class Home extends React.Component {
  static propTypes = {
    isMobile: PropTypes.bool.isRequired,
    background: PropTypes.string,
    eventolMessage: PropTypes.string,
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    user: PropTypes.shape({
      /* eslint-disable camelcase */
      first_name: PropTypes.string,
      last_name: PropTypes.string,
      /* eslint-enable camelcase */
    }),
  }

  static defaultProps = {
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
      const searchUrl = `?search=${searchTerm}&fields=${HOME_REQUIRED_FIELDS}`; /* TODO: move to utils */
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
        {searched && <TitleList showEmpty title={gettext('Search results')} url={searchUrl} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={`?my_events=true&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='recent'
          title={gettext('Recent Events')}
          url={`?ordering=-created_at&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='featured'
          title={gettext('Featured Events')}
          url={`?ordering=-attendees_count&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={`?registration_is_open=true&ordering=last_date&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='schedule_confirmed'
          title={gettext('Events with Confirmed Schedule')}
          url={`?schedule_confirmed=true&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='finished'
          title={gettext('Finished Events')}
          url={`?registration_is_open=false&ordering=-attendees_count&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
      </div>
    );
  }
}

const mapSizesToProps = ({width}) => ({
  isMobile: width < 950,
});

export default withSizes(mapSizesToProps)(Home);
