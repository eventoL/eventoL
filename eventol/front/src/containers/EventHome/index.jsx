import React from 'react';
import PropTypes from 'prop-types';
import withSizes from 'react-sizes';

import Hero from '../../components/Hero';
import Header from '../../components/Header';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import {
  getSearchUrl, getMyEventsUrl,
  getUpcommingEventsUrl,
  getFinishedEventsUrl,
} from '../../utils/urls';
import {
  MOBILE_WIDTH,
  BACKGROUND_DEFAULT,
  LOGO_HEADER_DEFAULT,
  LOGO_LANDING_DEFAULT,
} from '../../utils/constants';

import './index.scss';


class EventHome extends React.Component {
  static propTypes = {
    isMobile: PropTypes.bool.isRequired,
    background: PropTypes.string,
    logoHeader: PropTypes.string,
    logoLanding: PropTypes.string,
    tagMessage: PropTypes.string,
    tagSlug: PropTypes.string,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  }

  static defaultProps = {
    background: BACKGROUND_DEFAULT,
    logoHeader: LOGO_HEADER_DEFAULT,
    logoLanding: LOGO_LANDING_DEFAULT,
    tagMessage: null,
    tagSlug: null,
    user: null,
  }

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false,
  }

  handleOnEnter = () => {
    const {tagSlug} = this.props;
    const {searchTerm} = this.state;
    if (searchTerm !== ''){
      const searchUrl = getSearchUrl(searchTerm, tagSlug);
      this.setState({searchUrl, searched: true});
    }
  }

  handleOnChange = searchTerm => this.setState({searchTerm})

  render(){
    const {searched, searchUrl} = this.state;
    const {
      user, tagSlug, background,
      logoHeader, logoLanding,
      tagMessage, isMobile,
    } = this.props;
    return (
      <div>
        <Header logoHeader={logoHeader} user={user} isMobile={isMobile} />
        <Hero background={background} logoLanding={logoLanding} message={tagMessage} slug={tagSlug}>
          <Search onChange={this.handleOnChange} onEnter={this.handleOnEnter} />
        </Hero>
        {searched && <TitleList showEmpty id='search_results' title={gettext('Search results')} url={searchUrl} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={getMyEventsUrl(tagSlug)}
        />
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={getUpcommingEventsUrl(tagSlug)}
        />
        <TitleList
          id='finished'
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
