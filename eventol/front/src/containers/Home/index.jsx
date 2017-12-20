import React from 'react';
import Hero from '../../components/Hero';
import Header from '../../components/Header';
import Search from '../../components/Search';
import TitleList from '../../components/TitleList';
import './index.css';


export default class App extends React.Component {
  state = {
    searchTerm: '',
    searchUrl: '',
    searched: false
  };

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
        <TitleList title='Eventos Destacados' url='discover/tv?sort_by=popularity.desc&page=1' />
        <TitleList title='Tendencia actual' url='discover/movie?sort_by=popularity.desc&page=1' />
        <TitleList title='Mas recietes' url='genre/27/movies?sort_by=popularity.desc&page=1' />
        <TitleList title='Meetups' url='genre/878/movies?sort_by=popularity.desc&page=1' />
        <TitleList title='Festivales de Instalación' url='genre/35/movies?sort_by=popularity.desc&page=1' />
        <TitleList title='Conferencias' url='genre/35/movies?sort_by=popularity.desc&page=1' />
      </div>
    );
  }
};
