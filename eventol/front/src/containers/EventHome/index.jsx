import React from 'react'
import PropTypes from 'prop-types'
import Hero from '../../components/Hero'
import Header from '../../components/Header'
import Search from '../../components/Search'
import TitleList from '../../components/TitleList'
import {HOME_REQUIRED_FIELDS} from '../../utils/constants'

import './index.scss'


export default class EventHome extends React.Component {

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false
  }

  propTypes = {
    slug: PropTypes.string,
    user: PropTypes.object
  }

  onEnter = () => {
    const {slug} = this.props;
    const {searchTerm} = this.state;
    if (searchTerm !== '') {
      const searchUrl = `?search=${searchTerm}&slug=${slug}&fields=${HOME_REQUIRED_FIELDS}`;
      this.setState({searchUrl, searched: true});
    }
  }

  onChange = searchTerm => this.setState({searchTerm})

  render(){
    const {user, slug} = this.props;
    const {searched, searchUrl} = this.state;
    return (
      <div>
        <Header user={user}/>
        <Hero slug={slug}>
          <Search onChange={this.onChange} onEnter={this.onEnter} />
        </Hero>
        {searched && <TitleList title={gettext('Search results')} url={searchUrl} showEmpty={true} />}
        <TitleList
          id='next'
          title={gettext('Upcoming Events')}
          url={`?registration_is_open=true&ordering=last_date&slug=${slug}&fields=${HOME_REQUIRED_FIELDS}`} />
        <TitleList
          id='finished'
          title={gettext('Finished Events')}
          url={`?registration_is_open=false&ordering=-attendees_count&slug=${slug}&fields=${HOME_REQUIRED_FIELDS}`} />
      </div>
    );
  }
}
