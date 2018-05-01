import React from 'react'
import Hero from '../../components/Hero'
import Header from '../../components/Header'
import Search from '../../components/Search'
import TitleList from '../../components/TitleList'
import {HOME_REQUIRED_FIELDS} from '../../utils/constants'

import './index.scss'


export default class Home extends React.Component {

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false
  }

  onEnter = () => {
    const {searchTerm} = this.state;
    if (searchTerm !== '') {
      const searchUrl = `?search=${searchTerm}&fields=${HOME_REQUIRED_FIELDS}`;
      this.setState({searchUrl, searched: true});
    }
  }

  onChange = searchTerm => this.setState({searchTerm})

  render(){
    const {searched, searchUrl} = this.state;
    const {user} = this.props;
    return (
      <div>
        <Header user={user}/>
        <Hero>
          <Search onChange={this.onChange} onEnter={this.onEnter} />
        </Hero>
        {searched && <TitleList title={gettext('Search results')} url={searchUrl} showEmpty={true} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={`?my_events=true&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='recent'
          title={gettext('Recent Events')}
          url={`?ordering=-created_at&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='featured'
          title={gettext('Featured Events')}
          url={`?ordering=-attendees_count&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={`?registration_is_open=true&ordering=last_date&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='schedule_confirmed'
          title={gettext('Events with Confirmed Schedule')}
          url={`?schedule_confirmed=true&registration_is_open=true&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='finished'
          title={gettext('Finished Events')}
          url={`?registration_is_open=false&ordering=-attendees_count&fields=${HOME_REQUIRED_FIELDS}`} />
      </div>
    );
  }
}
