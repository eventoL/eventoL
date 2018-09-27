import React from 'react';
import PropTypes from 'prop-types';
import SliderItems from '../SliderItems';
import {getUrl} from '../../utils/api';

import './index.scss';


export default class TitleList extends React.Component {
  static propTypes = {
    id: PropTypes.string,
    showEmpty: PropTypes.bool,
    title: PropTypes.string,
    url: PropTypes.string
  }

  state = {
    data: [],
    mounted: false
  }

  componentDidMount(){
    const {url} = this.props;
    if(url !== ''){
      this.loadContent();
      this.setState({mounted: true});
    }
  }

  componentWillReceiveProps({url}){
    const {url: prevUrl} = this.props;
    if(url !== prevUrl && url !== ''){
      this.setState({mounted: true, url}, ()=>{
        this.loadContent();
      });
    }
  }

  loadContent(){
    const {url} = this.props;
    const fullUrl = `/api/events/${url}`;
    getUrl(fullUrl)
      .then(data => this.setState({data}))
      .catch(err => console.error('There has been an error', err));
  }

  parseItem({tags, event_slug, place, image:backdrop, name:title, attendees_count:attendees, abstract:overview}){
    if (backdrop){
      backdrop = new URL(backdrop).pathname;
    }
    return {
      event_slug, title, attendees, overview, backdrop, place, tags,
      key: event_slug, url: `/events/${event_slug}/`
    };
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
      }; // TODO: move to constant
      return (
        <div className='title-list' data-loaded={mounted} id={id}>
          <div className='category-title'>
            <h1>{title}</h1>
            <SliderItems itemsData={[emptyItem]} />
          </div>
        </div>
      );
    }
    return (
      <div className='title-list' data-loaded={mounted} id={id}>
        <div className='category-title'>
          <h1>{title}</h1>
          <SliderItems itemsData={itemsData} sliderId={id} />
        </div>
      </div>
    );
  }
}
