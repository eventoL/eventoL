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
      const searchUrl = `?search=${searchTerm}`;
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
        <TitleList id='recientes' title='Eventos Recientes' url='?ordering=-created&registration_is_open=true' />
        <TitleList id='destacados' title='Eventos Destacados' url='?ordering=-attendees_count&registration_is_open=true' />
        <TitleList id='proximos' title='Proximos Eventos' url='?registration_is_open=true&ordering=last_date' />
        <TitleList id='cronograma_confirmado' title='Eventos con Cronograma Confirmado' url='?schedule_confirmed=true&registration_is_open=true' />
        <TitleList id='finalizados' title='Eventos Finalizados' url='?registration_is_open=false&ordering=-attendees_count' />
      </div>
    );
  }
};
