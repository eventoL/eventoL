import React from 'react'
import Hero from '../../components/Hero'
import Header from '../../components/Header'
import Search from '../../components/Search'
import TitleList from '../../components/TitleList'

import './index.css'


export default class App extends React.Component {

  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false
  }

  onEnter = () => {
    const {searchTerm} = this.state;
    if (searchTerm !== '') {
      const searchUrl = `search/multi?query=${searchTerm}`;
      this.setState({searchUrl, searched: true});
    }
  }

  onChange = searchTerm => this.setState({searchTerm})

  render(){
    const {searched, searchUrl} = this.state;
    return (
      <div>
        <Header />
        <Hero>
          <Search onChange={this.onChange} onEnter={this.onEnter} />
        </Hero>
        {searched && <TitleList title='Resultados de busqueda' url={searchUrl} />}
        <TitleList title='Eventos Destacados' url='?ordering=attendees_count' />
        <TitleList title='Proximos eventos' url='?ordering=last_date' />
      </div>
    );
  }
};
