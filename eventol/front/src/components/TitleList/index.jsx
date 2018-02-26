import React from 'react';

import SliderItems from '../SliderItems';

import './index.css';


export default class TitleList extends React.Component {
  state = {
    data: [],
    mounted: false
  };

  loadContent(){
    const url = `/api/events/${this.props.url}`;
    console.log('url', url);
    fetch(url)
      .then(response => response.json())
      .then(data => this.setState({data}))
      .catch(err => console.log("There has been an error", err));
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

  parseItem({title, slug, place, image:backdrop, attendees_count:attendees, abstract:overview}){
    return {
      title, attendees, overview, backdrop, slug, place,
      key: slug, url: `/event/${slug}/`
    }
  }

  render(){
    const {title, id} = this.props;
    const {mounted, data: {results}} = this.state;
    let itemsData = '';
    if(results) {
      itemsData = results.map(this.parseItem);
    }
    if (!itemsData || itemsData.length === 0) return null;
    return (
      <div id={id} ref="titlecategory" className="TitleList" data-loaded={mounted}>
        <div className="CategoryTitle">
          <h1>{title}</h1>
          <SliderItems itemsData={itemsData}/>
        </div>
      </div>
    );
  }
};
