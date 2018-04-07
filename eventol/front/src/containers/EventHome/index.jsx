import React from 'react'
import Hero from '../../components/Hero'
import Header from '../../components/Header'
import Search from '../../components/Search'
import TitleList from '../../components/TitleList'

import './index.scss'


export default class EventHome extends React.Component {

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false
  }

  onEnter = () => {
    const {searchTerm} = this.state;
    if (searchTerm !== '') {
      const searchUrl = `?search=${searchTerm}`;
      this.setState({searchUrl, searched: true});
    }
  }

  onChange = searchTerm => this.setState({searchTerm})

  render(){
    const {searched, searchUrl} = this.state;
    const {user, slug} = this.props;
    return (
      <div>
        <Header user={user}/>
        <Hero slug={slug}>
          <Search onChange={this.onChange} onEnter={this.onEnter} />
        </Hero>
        {searched && <TitleList title={gettext('Search results')} url={searchUrl} showEmpty={true} />}
        <TitleList
          id='my_events'
          title={gettext('My Events')}
          url={`?my_events=true&slug=${slug}`} />
        <TitleList
          id='recent'
          title={gettext('Recent Events')}
          url={`?ordering=-created_at&registration_is_open=true&slug=${slug}`} />
        <TitleList
          id='featured'
          title={gettext('Featured Events')}
          url={`?ordering=-attendees_count&registration_is_open=true&slug=${slug}`}/>
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={`?registration_is_open=true&ordering=last_date&slug=${slug}`} />
        <TitleList
          id='schedule_confirmed'
          title={gettext('Events with Confirmed Schedule')}
          url={`?schedule_confirmed=true&registration_is_open=true&slug=${slug}`} />
        <TitleList
          id='finished'
          title={gettext('Finished Events')}
          url={`?registration_is_open=false&ordering=-attendees_count&slug=${slug}`} />
      </div>
    );
  }
};
