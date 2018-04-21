import React from 'react'
import SliderItems from '../SliderItems'
import {getUrl} from '../../utils/api'

import './index.scss'


export default class TitleList extends React.Component {
  state = {
    data: [],
    mounted: false
  };

  loadContent(){
    const url = `/api/events/${this.props.url}`;
    getUrl(url)
      .then(data => this.setState({data}))
      .catch(err => console.error('There has been an error', err));
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

  parseItem({uid, slug, place, image:backdrop, name:title, attendees_count:attendees, abstract:overview}){
    if (backdrop){
      backdrop = new URL(backdrop).pathname;
    }
    return {
      uid, title, attendees, overview, backdrop, slug, place,
      key: uid, url: `/event/${slug}/${uid}/`
    }
  }

  render(){
    const {title, id} = this.props;
    const {mounted, data: {results}} = this.state;
    let itemsData = '';
    if(results) {
      itemsData = results.map(this.parseItem);
    }
    if (!itemsData || itemsData.length === 0) {
      if (!this.props.hasOwnProperty('showEmpty') || !this.props.showEmpty) return null;
      const emptyItem = {
        key: 'not_found',
        title: gettext('Event not found'),
        overview: gettext('No Event found in your search'),
        backdrop: '/static/manager/img/logo.png'
      }
      return (<div id={id} ref="titlecategory" className="TitleList" data-loaded={mounted}>
        <div className="CategoryTitle">
          <h1>{title}</h1>
          <SliderItems itemsData={[emptyItem]}/>
        </div>
      </div>)
    }
    return (
      <div id={id} ref="titlecategory" className="TitleList" data-loaded={mounted}>
        <div className="CategoryTitle">
          <h1>{title}</h1>
          <SliderItems itemsData={itemsData} sliderId={id}/>
        </div>
      </div>
    );
  }

}
