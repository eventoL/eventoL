import React from 'react';
import Item from '../Item';
import './index.css';


export default class TitleList extends React.Component {
  state = {
    data: [],
    mounted: false
  };

  loadContent(){
    const url = `https://api.themoviedb.org/3/${this.props.url}&api_key=87dfa1c669eea853da609d4968d294be`;
    fetch(url)
      .then(response => response.json())
      .then(() => {
        const links = [
          {url: 'https://flisolbogota.org/wp-content/uploads/2015/06/cropped-LogoFLISoL2015-Negro.png', title: 'Flisol Bogota 2015', attendees: 500},
          {url: 'https://rogercv.files.wordpress.com/2015/03/flisol-2015.png', title: 'Flisol peru 2015', attendees: 600},
          {url: 'https://wiki.cafelug.org.ar/images/thumb/d/d2/FLISOL_logo_mail.png/400px-FLISOL_logo_mail.png', title: 'Flisol Argentina 2015', attendees: 550},
          {url: 'http://linware.com.ar/wp-content/uploads/2014/04/140414-3.jpg', title: 'Flisol 2014', attendees: 800},
          {url: 'http://www.radiohrn.hn/l/sites/default/files/styles/internas/public/festival.PNG?itok=Hue9wNzu', title: 'Flisol', attendees: 300},
        ]
        const data = {
          results: links.map(({title, url:backdrop_path, attendees}, index) => {
            return {
              id: index,
              overview: "El FLISoL es el evento de difusión de Software Libre más grande en Latinoamérica y está dirigido a todo tipo de público: estudiantes, académicos, empresarios, trabajadores, funcionarios públicos, entusiastas y aun personas que no poseen mucho conocimiento informático",
              title, attendees, backdrop_path
            }
          })
        }
        this.setState({data});
    }).catch(err => console.log("There has been an error"));
  }

  componentWillReceiveProps(nextProps){
    if(nextProps.url !== this.props.url && nextProps.url !== ''){
      this.setState({mounted: true, url: nextProps.url},()=>{
        this.loadContent();
      });
    }
  }

  componentDidMount(){
    if(this.props.url !== ''){
      this.loadContent();
      this.setState({mounted: true});
    }
  }

  render(){
    const {mounted, data: {results}} = this.state;
    const {title} = this.props;
    let titles = '';
    if(results) {
      titles = results.map(({id:key, title, attendees, overview, backdrop_path:backdrop}, i) => {
        if(i < 5) {
          const item = {key, title, attendees, overview, backdrop}
          return <Item {...item} />
        }
        return <div key></div>;
      });
    }
    return (
      <div ref="titlecategory" className="TitleList" data-loaded={mounted}>
        <div className="CategoryTitle">
          <h1>{title}</h1>
          <div className="titles-wrapper">
            {titles}
          </div>
        </div>
      </div>
    );
  }
};
