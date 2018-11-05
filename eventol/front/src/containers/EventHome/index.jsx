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
  HOME_REQUIRED_FIELDS,
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
      /* eslint-disable camelcase */
      first_name: PropTypes.string,
      last_name: PropTypes.string,
      /* eslint-enable camelcase */
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
      const searchUrl = `?search=${searchTerm}&tags__slug=${tagSlug}&fields=${HOME_REQUIRED_FIELDS}`; // TODO: move to utils
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
        {searched && <TitleList showEmpty title={gettext('Search results')} url={searchUrl} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={`?my_events=true&tags__slug=${tagSlug}&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={`?registration_is_open=true&ordering=last_date&tags__slug=${tagSlug}&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
        <TitleList
          id='finished'
          title={gettext('Finished Events')}
          url={`?registration_is_open=false&ordering=-attendees_count&tags__slug=${tagSlug}&fields=${HOME_REQUIRED_FIELDS}` /* TODO: move to utils */}
        />
      </div>
    );
  }
}

const mapSizesToProps = ({width}) => ({
  isMobile: width < MOBILE_WIDTH,
});

export default withSizes(mapSizesToProps)(EventHome);
